"""Build DADS M12 Lab 1 — Claude API & Tools."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from build_lab import build, md, code

LAB_PATH = Path("labs/M12/M12_Lab1_Claude_API_Tools.ipynb")
TITLE = "M12 Lab 1 — Claude API & Tools"
EMOJI = "🟧"
DIFFICULTY = "Intermediate"
TIME = "~40 min"

body = [
    md("""<div style="background: #f0f4ff; border-left: 4px solid #0055d4; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0;">
  <h3 style="color: #001a70; margin: 0 0 8px;">🎯 Learning Objectives</h3>
  <ol style="margin: 0; color: #1a1a2e; font-size: 14px;">
    <li>Make your <b>first call</b> to the Anthropic Claude API</li>
    <li>Understand the <b>differences</b> from OpenAI's chat API (system messages, message shape, content blocks)</li>
    <li>Use Claude's <b>tool use</b> feature to give the model a calculator and have it actually call it</li>
    <li>Stream a <b>multi-turn tool conversation</b> end to end</li>
  </ol>
</div>
"""),

    md("""## 🟧 Why a separate lab for Claude?

You've spent the course inside OpenAI's ecosystem. The principles transfer one-to-one — chat completions, system prompts, tool calling — but the **API shape is different**, and "different" means a thousand small bugs the first time you switch providers. This lab gets you fluent in Anthropic's SDK so adding Claude as a fallback or a primary model in your own apps is a 10-minute swap, not a week.
"""),

    md("""## 1️⃣ Setup — install + key

The `anthropic` package is on PyPI. The key is `ANTHROPIC_API_KEY` — set it as a Colab secret (🔑 sidebar) the same way you set `OPENAI_API_KEY`.
"""),

    code("""import importlib.util, os
if importlib.util.find_spec("anthropic") is None:
    !pip install -q anthropic

# Pull the key from the same Colab secret pattern DADS uses everywhere.
try:
    from google.colab import userdata
    os.environ["ANTHROPIC_API_KEY"] = userdata.get("ANTHROPIC_API_KEY") or ""
except (ImportError, ModuleNotFoundError):
    pass

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise EnvironmentError("ANTHROPIC_API_KEY not found. In Colab: 🔑 sidebar → add a secret named ANTHROPIC_API_KEY.")

from anthropic import Anthropic
claude = Anthropic()
print("Anthropic client ready")
"""),

    md("""## 2️⃣ First call — chat completion

Note three things compared to OpenAI:
1. The method is `client.messages.create(...)`, not `chat.completions.create(...)`.
2. The **system prompt is a top-level argument**, not a message in the array.
3. `max_tokens` is **required** (Anthropic considers it part of the contract).
"""),

    code("""CLAUDE_MODEL = "claude-sonnet-4-6"   # latest Sonnet 4.x at the time of writing

resp = claude.messages.create(
    model=CLAUDE_MODEL,
    max_tokens=300,
    system="You are a precise technical writer. Answer in two sentences.",
    messages=[
        {"role": "user", "content": "What is the difference between Anthropic's Sonnet and Opus tiers?"}
    ],
)

# Anthropic responses are a list of content blocks; for plain text replies
# the first block is text.
text = resp.content[0].text
pretty_print(text, title="🟧 Claude reply", theme="yellow")
print(f"input tokens: {resp.usage.input_tokens}  |  output tokens: {resp.usage.output_tokens}")
"""),

    md("""## 3️⃣ Multi-turn — passing history back

Same shape as OpenAI: append every assistant reply to your `messages` list and send it back next turn. There's no built-in conversation state on the server.
"""),

    code("""history = [
    {"role": "user", "content": "Hi! I'm preparing a graduate course on Generative AI."},
]

r1 = claude.messages.create(model=CLAUDE_MODEL, max_tokens=200, system="You are a helpful TA.", messages=history)
history.append({"role": "assistant", "content": r1.content[0].text})

history.append({"role": "user", "content": "Suggest one good final-project topic for that course."})
r2 = claude.messages.create(model=CLAUDE_MODEL, max_tokens=200, system="You are a helpful TA.", messages=history)

pretty_print(r1.content[0].text, title="Turn 1", theme="yellow")
pretty_print(r2.content[0].text, title="Turn 2", theme="yellow")
"""),

    md("""## 4️⃣ Tool use — give Claude a calculator

The pattern (called *tool use* by Anthropic, *function calling* by OpenAI) is the same idea:
1. **You** describe a tool with name + input schema.
2. **The model** decides whether to call it; if yes, it returns a `tool_use` content block with arguments.
3. **You** run the tool, then send a `tool_result` content block back so the model can finish.

We'll wire a tiny calculator and watch the model use it on a question that requires arithmetic.
"""),

    code("""TOOLS = [
    {
        "name": "calculator",
        "description": (
            "Evaluate a basic arithmetic expression. Use ONLY for math the user asked about. "
            "Supports +, -, *, /, parentheses, and integer/decimal numbers."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "An arithmetic expression to evaluate, e.g. '17.5 * 12'."}
            },
            "required": ["expression"],
        },
    }
]

def run_calculator(expression: str) -> str:
    \"\"\"Tiny safe-ish evaluator: only arithmetic chars allowed.\"\"\"
    import re
    if not re.fullmatch(r"[0-9+\\-*/(). ]+", expression):
        return "ERROR: only basic arithmetic characters allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"ERROR: {e}"
"""),

    code("""def chat_with_tools(user_message: str, max_iters: int = 4) -> str:
    \"\"\"Run a tool-use loop until Claude returns a final assistant message.\"\"\"
    msgs = [{"role": "user", "content": user_message}]
    for step in range(max_iters):
        resp = claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=400,
            tools=TOOLS,
            messages=msgs,
        )

        # If the stop reason isn't a tool call, we're done.
        if resp.stop_reason != "tool_use":
            return next((b.text for b in resp.content if b.type == "text"), "(no text)")

        # Otherwise: append the assistant turn (with the tool_use block) verbatim,
        # then run each tool the model asked for and append a tool_result for each.
        msgs.append({"role": "assistant", "content": resp.content})

        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                print(f"[step {step}] Claude called {block.name}({block.input})")
                output = run_calculator(**block.input) if block.name == "calculator" else f"unknown tool {block.name}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        msgs.append({"role": "user", "content": tool_results})

    return "(loop limit reached)"

answer = chat_with_tools(
    "I'm planning a course with 14 modules. If each module needs 3 hours of recording and post takes 5x, how many post hours total?"
)
pretty_print(answer, title="🧮 Final answer (with tool use)", theme="green")
"""),

    md("""## 5️⃣ Compare with OpenAI on the same question

A direct A/B between Claude and the OpenAI chat default. Same prompt, same task — different reasoning styles.
"""),

    code("""openai_resp = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    messages=[{
        "role": "user",
        "content": "I'm planning a course with 14 modules. If each module needs 3 hours of recording and post takes 5x, how many post hours total?"
    }],
)

compare_responses({
    f"Claude · {CLAUDE_MODEL}": answer,
    f"OpenAI · {DEFAULT_CHAT_MODEL}": openai_resp.choices[0].message.content,
})
"""),

    md("""## 🎯 Hands-on exercise

1. **Add a `web_search`-style tool** (mocked — return canned results) and wire it into the loop alongside `calculator`. Ask Claude a question that requires both.
2. Switch to `claude-haiku-4-5` for the same calculator task. Does the cheaper model still call the tool correctly?
3. Try sending a **multi-turn** tool conversation (two arithmetic questions in a row). Inspect the `msgs` list — what did Claude remember between turns?

> 💡 The tool-use protocol is identical conceptually to OpenAI's function calling — only the field names change. Once you've internalized it for one provider, the other is a 10-minute read of the docs.
"""),

    code("""# Your turn.
"""),

    md("""---
*Next lab — the M12 Lab 2 self-study supplement covers Google's A2A protocol and OpenAI's Agents SDK. Same patterns, three platforms.*
"""),
]

if __name__ == "__main__":
    build(LAB_PATH, TITLE, EMOJI, DIFFICULTY, TIME, body)
