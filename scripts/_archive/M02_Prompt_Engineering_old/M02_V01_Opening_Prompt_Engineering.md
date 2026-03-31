======================================================
MODULE: M02 — Prompt Engineering
VIDEO: Opening — The Art and Science of Prompting
NARRATOR: Prof. Dehghani
DURATION: 4.5 minutes (~500 words)
======================================================

PART 1: OPENING HOOK
------------------------

Every morning I place the same coffee order: medium dark roast, whole milk on the side, cinnamon on top. My barista knows it by heart. I never have to explain myself twice.

That is exactly the standard we should hold ourselves to when we write prompts for an AI model.

Think about what makes that coffee order work. It is specific. It is structured. There is no ambiguity. My barista does not have to guess whether I want cream or milk. She does not have to ask what size. Every detail is there.

Now think about what happens when someone walks up to the counter and says, "Just give me a coffee." They get whatever the barista decides. Maybe it is good. Maybe it is not what they wanted at all. They have no one to blame but themselves.

That is the difference between a vague prompt and a well-engineered one. And here is the key part: the quality of what a large language model gives you depends almost entirely on the quality of the instructions you give it.

[ANIMATION: Simple flow diagram — User -> Prompt -> LLM -> Output, with a "quality in = quality out" label]

PART 2: THE THREE-LAYER FRAMEWORK
------------------------

Before we can improve our prompts, we need to understand their structure. Every prompt sent to a large language model API has three components.

The first is the System layer. This defines the model's role, persona, or behavioral constraints. For example: "You are a data analyst who provides concise, evidence-based responses and avoids speculation."

The second is the User layer. This is the actual request. It tells the model what you need it to do. For example: "Summarize the three most significant findings in this quarterly earnings report."

The third is the Assistant layer. This captures the model's prior responses. In multi-turn conversations, it can also be pre-filled to guide how the model continues.

Together, these three components form the anatomy of every API call you will build in this course.

[ANIMATION: Three stacked layers diagram — System (top, blue), User (middle, green), Assistant (bottom, gray) — each with its example text]

PART 3: FOUR ESSENTIAL ELEMENTS
------------------------

Beyond the three-layer structure, a well-crafted prompt should consistently include four elements.

Role. Define who the model is acting as. This sets the behavioral frame for the entire response.

Task. Specify exactly what needs to be done. Ambiguity here produces ambiguous outputs.

Context. Provide relevant background, constraints, or data. The model cannot assume information that is not in the prompt.

Format. Indicate the expected output structure: a numbered list, a JSON object, a paragraph, a table. If you do not specify a format, the model will choose one for you, and it may not be what you need.

[ANIMATION: Four quadrant graphic — Role, Task, Context, Format — each with a one-line example]

PART 4: PROMPTING STRATEGIES
------------------------

Now let us look at three foundational strategies.

Zero-shot prompting means asking the model to complete a task with no examples. You rely entirely on the model's existing knowledge. This works for straightforward tasks like translation or simple summarization.

Few-shot prompting means including one or more labeled examples before your actual question. This guides the model toward the reasoning style, tone, or format you expect.

Chain-of-thought prompting instructs the model to reason through the problem step by step before arriving at a final answer. Research from Google and OpenAI has shown this significantly improves performance on multi-step reasoning and mathematical tasks.

PART 5: WHY THIS MATTERS FOR YOUR CAREER
------------------------

These strategies are not academic exercises. In 2025 and 2026, organizations across industries are embedding structured prompt engineering directly into their production workflows. Well-designed prompts are the difference between a system that performs reliably at scale and one that produces inconsistent results requiring constant human correction.

In the labs this week, you will apply all three strategies across different task types, including sentiment analysis, mathematical reasoning, and content generation. You will compare the outputs directly and see for yourself how much structure matters.

The coffee order is your mental model. Be specific. Be structured. Leave nothing to chance.

======================================================
DIGITAL MEDIA NOTES:
- Opening: consider a brief coffee shop B-roll or illustrated coffee cup graphic during the analogy
- Three-layer diagram: make this a reusable graphic — it will appear again in later modules
- Four elements quadrant: animate each quadrant appearing one at a time as Prof. Dehghani names them
- Strategy overview: simple side-by-side comparison showing same prompt in zero-shot, few-shot, and chain-of-thought formats
- Embedded quiz opportunity: "Which prompting strategy uses labeled examples?" (Multiple choice)
======================================================
