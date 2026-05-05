"""Build DADS M13 Lab 2 — Output Filtering & Guardrails."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from build_lab import build, md, code

LAB_PATH = Path("labs/M13/M13_Lab2_Output_Filtering_Guardrails.ipynb")
TITLE = "M13 Lab 2 — Output Filtering & Guardrails"
EMOJI = "🚧"
DIFFICULTY = "Intermediate"
TIME = "~40 min"

body = [
    md("""<div style="background: #f0f4ff; border-left: 4px solid #0055d4; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0;">
  <h3 style="color: #001a70; margin: 0 0 8px;">🎯 Learning Objectives</h3>
  <ol style="margin: 0; color: #1a1a2e; font-size: 14px;">
    <li>Use OpenAI's <b>Moderation endpoint</b> to score text for harm categories</li>
    <li>Build a <b>policy engine</b> that combines moderation + custom rules</li>
    <li>Implement <b>topic / scope guardrails</b> ("only answer about X")</li>
    <li>Wire pre- and post-LLM checks into a single <b>safe response</b> function</li>
  </ol>
</div>
"""),

    md("""## 🚧 Why guardrails

The model will say almost anything if you ask the right way. That's not a bug — it's the default behavior of a system trained to be helpful. *Your app* is what decides what's allowed. Guardrails are how you draw that line in code.

This lab builds the three layers every production system needs:
1. **Moderation classifier** — does this content cross a hard line?
2. **Custom policy** — does this match a rule unique to my product?
3. **Topic / scope guardrail** — is this even something my app should answer?
"""),

    md("""## 1️⃣ OpenAI Moderation endpoint

Free. No prompt engineering. Returns scores for ~12 harm categories (hate, harassment, self-harm, sexual, violence, illicit, etc.). Use this as your first line of defense on user inputs **and** on model outputs.
"""),

    code("""def moderate(text: str) -> dict:
    r = client.moderations.create(model="omni-moderation-latest", input=text)
    out = r.results[0]
    return {
        "flagged": out.flagged,
        # category_scores is a Pydantic-ish object; pull non-zero scores into a tidy dict
        "scores": {k: round(v, 4) for k, v in out.category_scores.model_dump().items() if v > 0.01},
        "categories": [k for k, v in out.categories.model_dump().items() if v],
    }

# Three samples: benign, borderline, clearly disallowed.
samples = [
    "What is the capital of France?",
    "I'm writing a thriller; describe a violent fistfight scene.",
    "Step-by-step instructions to build a working pipe bomb.",
]
for s in samples:
    pp({"text": s[:60], **moderate(s)}, title="moderation result")
"""),

    md("""## 2️⃣ Custom policy rules

Moderation handles the universal stuff. *Your* policy handles the product-specific stuff: "no medical diagnoses," "no investment advice," "no full source code dumps." We express these as a list of (regex_or_keyword, label, action) tuples.
"""),

    code("""import re

POLICY_RULES = [
    # (matcher, label, action)
    (re.compile(r"\\b(diagnosis|prescribe|medical advice)\\b", re.I), "medical_advice", "block"),
    (re.compile(r"\\b(buy|sell|short)\\s+(?:the\\s+)?(?:stock|crypto)", re.I), "investment_recommendation", "warn"),
    (re.compile(r"\\b(internal|confidential|proprietary)\\b", re.I), "sensitive_label", "warn"),
]

def apply_policy(text: str) -> dict:
    hits = []
    for pat, label, action in POLICY_RULES:
        m = pat.search(text)
        if m:
            hits.append({"label": label, "action": action, "match": m.group(0)})
    blocked = any(h["action"] == "block" for h in hits)
    return {"hits": hits, "blocked": blocked}

print(apply_policy("Should I buy the stock based on this?"))
print(apply_policy("Give me a medical diagnosis for these symptoms."))
print(apply_policy("How do I build a Flask API?"))
"""),

    md("""## 3️⃣ Topic / scope guardrail

The most underused defense: just refuse to answer off-topic questions. We use a tiny LLM-as-judge call to classify whether the user's question fits our app's scope.
"""),

    code("""APP_SCOPE = (
    "This assistant ONLY answers questions about Python programming and the OpenAI / Anthropic / "
    "Google APIs. Anything else is out of scope."
)

def in_scope(user_message: str) -> dict:
    r = client.chat.completions.create(
        model=DEFAULT_MINI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    f"{APP_SCOPE}\\n\\n"
                    'Decide if the user question is in scope. Return JSON: {"in_scope": bool, "reason": "<short>"}.'
                ),
            },
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    import json
    return json.loads(r.choices[0].message.content)

for q in ["How do I stream tokens from the OpenAI API?", "What's the capital of Mongolia?", "Compare Sonnet and Haiku tiers."]:
    pp({"q": q, **in_scope(q)}, title="scope check")
"""),

    md("""## 4️⃣ The full guardrail pipeline

Compose the three layers into one `safe_chat` function. Order matters:
1. Moderation on input — kill obvious abuse before paying any inference cost.
2. Scope check — soft refuse with a friendly message if off-topic.
3. Custom policy on input — block hard-disallowed topics.
4. Run the LLM.
5. Moderation on output — catch jailbreaks that produced disallowed content.
6. Custom policy on output — last-mile safety net.
"""),

    code("""REFUSAL = "I can't help with that. This assistant only handles questions about Python and the OpenAI / Anthropic / Google APIs."

def safe_chat(user_message: str) -> str:
    # 1. Input moderation
    mod_in = moderate(user_message)
    if mod_in["flagged"]:
        return f"❌ Input blocked by moderation. Categories: {mod_in['categories']}"

    # 2. Scope check
    scope = in_scope(user_message)
    if not scope["in_scope"]:
        return f"⚠ {REFUSAL}\\n(reason: {scope['reason']})"

    # 3. Input policy
    pol_in = apply_policy(user_message)
    if pol_in["blocked"]:
        return f"❌ Input blocked by policy. Hits: {pol_in['hits']}"

    # 4. Run model
    r = client.chat.completions.create(
        model=DEFAULT_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a Python and AI-API teaching assistant. Be concise and concrete."},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    raw = r.choices[0].message.content

    # 5. Output moderation
    mod_out = moderate(raw)
    if mod_out["flagged"]:
        return f"❌ Output suppressed by moderation (categories: {mod_out['categories']})"

    # 6. Output policy
    pol_out = apply_policy(raw)
    if pol_out["blocked"]:
        return f"❌ Output suppressed by policy. Hits: {pol_out['hits']}"

    # Pass.
    if pol_out["hits"]:
        raw += f"\\n\\n⚠ note: {len(pol_out['hits'])} policy warning(s) — {[h['label'] for h in pol_out['hits']]}"
    return raw
"""),

    code("""for q in [
    "How do I stream tokens from the OpenAI API?",
    "What is the meaning of life?",
    "Should I buy NVDA stock today?",
    "Diagnose my chest pain.",
]:
    pretty_print(safe_chat(q), title=f"Q: {q}", theme="blue")
"""),

    md("""## 🎯 Hands-on exercise

1. **Tune the scope** — change `APP_SCOPE` to something narrower (e.g. only your own course content). Re-test the four sample questions.
2. **Add a hate-speech custom rule** with a `block` action and a friendly refusal message.
3. **Add an output length guard**: any reply over 1500 characters gets truncated and a warning appended.
4. Reflect: which layer fires the most in your tests, and is that the layer that gives the best UX?

> 💡 Real apps log every guardrail decision. Add a tiny logger that records `(timestamp, layer, action, snippet)` to a list and print the last 10 calls at the end.
"""),

    code("""# Your turn.
"""),

    md("""---
*That's the safety stack. From here you'd combine it with auth, rate limiting, and audit logs to ship something defensible. Module M14 is your final project — go build it.*
"""),
]

if __name__ == "__main__":
    build(LAB_PATH, TITLE, EMOJI, DIFFICULTY, TIME, body)
