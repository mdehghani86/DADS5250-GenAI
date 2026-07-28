"""Build DADS M10 Lab 2 — LLM Evaluation."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from build_lab import build, md, code

LAB_PATH = Path("labs/M10/M10_Lab2_LLM_Evaluation.ipynb")
TITLE = "M10 Lab 2 — LLM Evaluation"
EMOJI = "📏"
DIFFICULTY = "Intermediate"
TIME = "~45 min"

body = [
    md("""<div style="background: #f0f4ff; border-left: 4px solid #0055d4; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0;">
  <h3 style="color: #001a70; margin: 0 0 8px;">🎯 Learning Objectives</h3>
  <ol style="margin: 0; color: #1a1a2e; font-size: 14px;">
    <li>Build a small <b>evaluation harness</b>: dataset → model → scoring → leaderboard</li>
    <li>Use <b>three scoring strategies</b>: exact-match, semantic similarity (embeddings), LLM-as-judge</li>
    <li>Compare <b>three models</b> (chat / mini / Gemini) on the same task</li>
    <li>Visualize results as a <b>scoreboard chart</b></li>
  </ol>
</div>

> **Why care?** Anyone can pick a model. Engineers measure the model.
"""),

    md("""## 🧠 The eval mindset

If you ship LLM features without evaluation, you ship vibes. Real teams treat the model like any other component: hold it to a fixed dataset, score every change, and watch the number move. This lab is the smallest version of that loop you can run in 30 minutes.

We'll evaluate three models on a tiny QA task using three different scoring methods, then chart who wins.
"""),

    md("""## 1️⃣ The eval set

Ten short factual questions with known correct answers. In a real project this is a CSV with hundreds of rows curated by your domain experts; the harness logic is the same.
"""),

    code("""EVAL_SET = [
    {"q": "What is the capital of France?", "a": "Paris"},
    {"q": "How many sides does a hexagon have?", "a": "6"},
    {"q": "What language was Python originally implemented in?", "a": "C"},
    {"q": "Who wrote 'The Old Man and the Sea'?", "a": "Ernest Hemingway"},
    {"q": "What is the chemical symbol for sodium?", "a": "Na"},
    {"q": "In what year did the Berlin Wall fall?", "a": "1989"},
    {"q": "What is the boiling point of water at sea level in Celsius?", "a": "100"},
    {"q": "Which planet has the most moons (as of 2024)?", "a": "Saturn"},
    {"q": "What is the SI unit of electric current?", "a": "ampere"},
    {"q": "Who painted the ceiling of the Sistine Chapel?", "a": "Michelangelo"},
]
print(f"{len(EVAL_SET)} questions loaded")
"""),

    md("""## 2️⃣ Run all questions through three models

Same prompt, three models. We instruct each to answer in **one short phrase** so scoring is tractable.
"""),

    code("""SYSTEM_PROMPT = "Answer in one short phrase. No explanation, no preamble, no punctuation beyond the answer itself."

def ask_openai(model: str, question: str) -> str:
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return r.choices[0].message.content.strip()

# Two OpenAI models for comparison.
MODELS = {
    "openai-chat": DEFAULT_CHAT_MODEL,
    "openai-mini": DEFAULT_MINI_MODEL,
}

import time
results = {label: [] for label in MODELS}
for label, model in MODELS.items():
    print(f"running {label} ({model}) ...")
    t0 = time.time()
    for row in EVAL_SET:
        results[label].append({"q": row["q"], "expected": row["a"], "got": ask_openai(model, row["q"])})
    print(f"  done in {time.time()-t0:.1f}s")

# Add Gemini.
gemini = setup_gemini()
print(f"running gemini ({DEFAULT_GEMINI_MODEL}) ...")
results["gemini"] = []
t0 = time.time()
for row in EVAL_SET:
    g = gemini.models.generate_content(
        model=DEFAULT_GEMINI_MODEL,
        contents=f"{SYSTEM_PROMPT}\\n\\nQuestion: {row['q']}",
    )
    results["gemini"].append({"q": row["q"], "expected": row["a"], "got": g.text.strip()})
print(f"  done in {time.time()-t0:.1f}s")
"""),

    md("""## 3️⃣ Scorer 1 — Exact match (case-insensitive, strip punctuation)

The crudest possible scorer. Catches "Paris" vs "Paris", misses "Paris, France."
"""),

    code("""import re

def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()

def exact_match(expected: str, got: str) -> int:
    return int(normalize(expected) == normalize(got))

# Show a small table of who got what.
import pandas as pd
rows = []
for label, runs in results.items():
    for r in runs:
        rows.append({
            "model": label,
            "question": r["q"][:50],
            "expected": r["expected"],
            "got": r["got"][:60],
            "exact": exact_match(r["expected"], r["got"]),
        })
df = pd.DataFrame(rows)
df.head(15)
"""),

    md("""## 4️⃣ Scorer 2 — Semantic similarity (embeddings)

Embeddings let us score "Paris" vs "Paris, France" as a near-match. We embed the expected and the got, then take cosine similarity.
"""),

    code("""import numpy as np

def embed_batch(texts):
    r = client.embeddings.create(model=DEFAULT_EMBED_MODEL, input=texts)
    return np.array([d.embedding for d in r.data])

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

# Embed all unique strings in one call to save round-trips.
unique_strings = list({s for r in df.itertuples() for s in (r.expected, r.got)})
emb = dict(zip(unique_strings, embed_batch(unique_strings)))

df["semantic"] = [cosine(emb[r.expected], emb[r.got]) for r in df.itertuples()]
df.head(10)
"""),

    md("""## 5️⃣ Scorer 3 — LLM-as-judge

The state-of-the-art scoring approach for free-form answers. We ask an LLM to read the expected and got and call it correct or incorrect, with a one-line reason. Use a *different* model for the judge than for the contestant when you can — here we just use the chat default for everyone since the eval is small.
"""),

    code("""def llm_judge(question: str, expected: str, got: str) -> dict:
    r = client.chat.completions.create(
        model=DEFAULT_CHAT_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict but fair grader. The student answered a factual question. "
                    "Mark it correct if the student's answer is factually equivalent to the expected one — "
                    "extra detail that's still correct is fine, but wrong facts are not. "
                    'Return JSON: {"correct": bool, "reason": "<short>"}'
                ),
            },
            {"role": "user",
             "content": f"Question: {question}\\nExpected: {expected}\\nGot: {got}"},
        ],
        temperature=0,
    )
    import json
    return json.loads(r.choices[0].message.content)

# Score the full df with the judge (small set, so it's cheap).
import json
judgments = []
for r in df.itertuples():
    j = llm_judge(r.question, r.expected, r.got)
    judgments.append({"judge_correct": int(bool(j["correct"])), "judge_reason": j.get("reason", "")})
df = pd.concat([df.reset_index(drop=True), pd.DataFrame(judgments)], axis=1)
df.head(10)
"""),

    md("""## 6️⃣ Scoreboard"""),

    code("""scoreboard = df.groupby("model").agg(
    exact_match_rate=("exact", "mean"),
    semantic_avg=("semantic", "mean"),
    judge_match_rate=("judge_correct", "mean"),
).round(3).sort_values("judge_match_rate", ascending=False)
pp(scoreboard.to_dict(orient="index"), title="🏁 Scoreboard")
scoreboard
"""),

    md("""## 7️⃣ Visual leaderboard"""),

    code("""import matplotlib.pyplot as plt
import numpy as np

models = scoreboard.index.tolist()
metrics = ["exact_match_rate", "semantic_avg", "judge_match_rate"]
labels = ["Exact match", "Semantic similarity", "LLM judge"]
colors = ["#001a70", "#0055d4", "#10b981"]

x = np.arange(len(models))
width = 0.26

fig, ax = plt.subplots(figsize=(10, 5))
for i, (metric, label, color) in enumerate(zip(metrics, labels, colors)):
    ax.bar(x + (i - 1) * width, scoreboard[metric].values, width, label=label, color=color)

ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Score")
ax.set_title("LLM evaluation — scores by metric", fontsize=13, fontweight="bold", color="#001a70")
ax.legend(frameon=False, loc="lower right")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
"""),

    md("""## 🎯 Hands-on exercise

1. **Add five questions of your own** to `EVAL_SET` covering a domain you care about (history, code, your major). Re-run the harness.
2. **Add a fourth model**: try the cheaper `gpt-5.4-nano` (yes, it exists) by adding it to the `MODELS` dict.
3. **Tighten the judge**: rewrite the judge's system prompt so it scores partial credit (0/0.5/1) instead of binary. How does the leaderboard change?
4. Reflect: which scorer matched your intuition best? Where do they disagree, and why?

> 💡 In real projects you'd freeze the eval set, run it on every model change, and watch the metric move over time — this is the smallest possible version of that loop.
"""),

    code("""# Your turn — extend EVAL_SET and re-run.
"""),

    md("""---
*This wraps M10. Next: M11 (Claude Code) and M12 (AI Platforms).*
"""),
]

if __name__ == "__main__":
    build(LAB_PATH, TITLE, EMOJI, DIFFICULTY, TIME, body)
