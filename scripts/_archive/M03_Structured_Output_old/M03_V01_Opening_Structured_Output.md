======================================================
MODULE: M03 — Structured Output & Function Calling
VIDEO: Opening — Structured Output
NARRATOR: Prof. Mohammad Dehghani
DURATION: 4-5 minutes (~500 words)
======================================================

PART 1: OPENING HOOK
------------------------

When I order a steak medium-rare, I do not want the chef to get creative. I want medium-rare. Not a deconstructed interpretation. Not a surprise tasting menu. Medium-rare. Done.

Structured output is the same idea.

You tell the model exactly what format to give you. JSON with these fields. An integer here, a string there, a list of three items. And the model delivers. No rambling. No extra commentary. Just the data you asked for, in the shape you asked for it.

This sounds simple. But it changes everything about how you build with AI.

[ANIMATION: Split screen — left side shows a messy paragraph of AI text, right side shows clean JSON with labeled fields snapping into place]


PART 2: WHAT IS STRUCTURED OUTPUT?
------------------------

Here is the problem. By default, a large language model gives you a wall of text. Natural language. Great for reading. Terrible for software.

If you are building an application — a dashboard, an API, a data pipeline — you need the output in a specific format. You need JSON. You need typed fields. You need guarantees.

That is what structured output gives you. You define a schema — this is the shape of the data I want — and the model is constrained to produce output that matches that schema exactly.

OpenAI calls this JSON mode and structured outputs. Under the hood, it uses something called constrained decoding. The model literally cannot generate tokens that would break your schema.

And then there is function calling. This is where it gets powerful. You describe a set of tools to the model — functions your code can execute — and the model decides when to call them and with what arguments. The model does not run the code. It generates the call. Your application executes it.

This is the bridge between AI and real software systems.

[ANIMATION: Flow diagram — User prompt enters model, model outputs structured JSON matching a Pydantic schema, JSON feeds into application code]


PART 3: REAL-WORLD EXAMPLES
------------------------

Let me give you two examples.

A healthcare company I know processes thousands of clinical notes every day. Free-text notes written by doctors. They use structured output to extract patient symptoms, diagnoses, and medications — as typed JSON objects — and feed them directly into their electronic health records system. What used to take a team of data entry specialists now runs in seconds.

In finance, JPMorgan built a system that reads contract documents and extracts key terms — party names, dates, obligations, penalties — using function calling. The model reads the document and calls an extraction function with the right arguments. No regex. No brittle rules. The model understands the document and structures the output.

[ANIMATION: Two panels — Clinical note transforming into clean JSON fields; Contract document with highlighted terms flowing into a structured table]


PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

Every production AI system needs structured output. Every single one. If you cannot get reliable, typed data out of a model, you cannot build anything real.

This is the skill that separates someone who plays with ChatGPT from someone who builds with it. Hiring managers want engineers who can connect AI to real systems. That connection is structured output and function calling.


PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will use JSON mode to extract structured data from messy text. You will define Pydantic models as output schemas. And you will build function-calling pipelines where the model decides which tools to invoke and your code executes them.

By the end of this module, your models will not just talk. They will produce data your applications can use.

Let us get into it.

======================================================
DIGITAL MEDIA NOTES:
- The steak/chef analogy could open with a quick 3-second clip or illustration of a restaurant order
- The JSON schema animation should show fields "snapping" into place like puzzle pieces
- Clinical notes example works well as a before/after split screen
- Consider embedding a 1-question poll: "Have you ever tried to parse free-text AI output with code?"
- End card: "Next: Lab — JSON Mode & Function Calling"
======================================================
