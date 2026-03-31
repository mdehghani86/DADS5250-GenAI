======================================================
MODULE: M01 — Getting Started with LLM APIs
FINAL SCRIPT (Teleprompter-Ready)
KEY MESSAGE: "The chat window is the demo. The API is the product."
Finalized: 2026-03-30
======================================================


VIDEO 1: "THE SPARK" (Opening, 3-4 min)
------------------------------------------------------

[ON CAMERA] OPENING HOOK (~40 sec)

There are two worlds of AI right now.

In one world, you open a browser, you type a question,
you get an answer. Nine hundred million people live in
this world.

In the other world, you write code. Your code talks
directly to the AI. It runs a thousand times while you
sleep. It connects to your data. It builds products.
Four million developers live in this world.

Today, you move from the first world to the second.

[ON CAMERA] KEY MESSAGE (~15 sec)

The chat window is the demo. The API is the product.
And this module teaches you to build the product.


======================================================

VIDEO 2: "WHAT ARE LLMs?" (Lecture, 6-8 min)
------------------------------------------------------

[VOICEOVER + ANIMATION] WHAT IS A LARGE LANGUAGE MODEL (~3 min)

LLM stands for Large Language Model. Here is what that
means.

Take a significant portion of human knowledge -- books,
code, research, conversations. Compress it into a
mathematical model. The model does not memorize any of
it. It learns patterns.

When you give it a prompt, it uses those patterns to
generate something new. Every response is original.
Every piece of code is composed, not retrieved. That is
generative AI -- and LLMs are the engine behind it.


[VOICEOVER + ANIMATION] PLATFORM VS API (~2 min)

You can access these models two ways.

The first is through a platform -- ChatGPT, Gemini,
Claude. You open a browser, type a message, get a
response. Think of it as walking into a restaurant and
ordering at the counter. It works. It is convenient.

The second way is through an API. Your Python code
sends a request directly to the model. Think of this as
building the delivery app -- you handle thousands of
orders, route them, process them, all automatically.
Same kitchen, same food, completely different power.


[VOICEOVER + ANIMATION] HOW LLMs GENERATE TEXT (~2 min)

Here is something worth understanding. LLMs do not
think. They predict.

When you send a prompt, the model looks at all the
words so far and calculates -- what is the most likely
next word? It picks one, adds it, and repeats. Word by
word. Token by token.

This is why temperature matters -- at zero, it always
picks the most likely word. At higher values, it takes
risks. And this is why LLMs sometimes hallucinate --
they generate text that sounds right but is factually
wrong.

The model does not know what is true. It knows what is
likely.


======================================================

VIDEO 3: "WHAT IS AN API?" (Lecture, 5-6 min)
------------------------------------------------------

[VOICEOVER + ANIMATION] API FROM ZERO (~3 min)

API stands for Application Programming Interface. Let
me make that simple.

Think of a vending machine. You put something in -- a
coin and a button press. Something happens inside that
you cannot see. And something comes out -- your drink.

You do not need to know how the machine works inside.
You just need to know two things: what to put in, and
what comes out.

An LLM API works the same way. You put in a prompt --
your question. Something happens on OpenAI's servers --
the model thinks. And out comes a response -- the
answer.


[VOICEOVER + CODE] THE CODE (~2 min)

Here is what it looks like in code.

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is an API?"}
    ]
)

print(response.choices[0].message.content)

Seven lines. That is all it takes. Seven lines and you
have programmatic access to one of the most powerful AI
models on earth.

Now imagine running those seven lines ten thousand
times in a loop. Or connecting them to a database. Or
triggering them from a web application. That is the
power of an API.


======================================================

VIDEO 4: "API SETUP GUIDE" (TA, 5-7 min)
------------------------------------------------------

[TA GUIDELINES]

Cover these steps:
1. OpenAI key: platform.openai.com -> API Keys -> Create
2. Gemini key: aistudio.google.com -> Get API Key
3. Colab Secrets: key icon -> store both keys
4. Two-line access code demo
5. Common errors: AuthenticationError, QuotaError, ModuleNotFoundError

Tone: Friendly, patient, step-by-step. Screen recording.


======================================================

VIDEO 5: "PARAMETERS, TOKENS & TEMPERATURE" (Transition, 3-5 min)
------------------------------------------------------

[VOICEOVER + ANIMATION] TRANSITION BETWEEN LABS

Before you start Lab 2, let us talk about what you are
actually controlling when you call the API.

Three things matter: temperature, tokens, and cost.

Temperature controls randomness. At zero, the model
gives you the same answer every time -- the most
predictable, most likely response. At one, it takes
more risks. At two, it gets creative -- sometimes too
creative.

Tokens are how LLMs measure text. Roughly four
characters per token, or about three-quarters of a
word. When you send a prompt, you pay for input tokens.
When the model responds, you pay for output tokens.

And the cost? GPT-4o Mini costs fifteen cents per
million input tokens. That is roughly seven hundred
fifty thousand words for fifteen cents. This technology
is remarkably cheap.

You will experiment with all of this in Lab 2.


======================================================

VIDEO 5b: LAB 1 WALKTHROUGH (Screen Recording, ~12 min)
------------------------------------------------------

[LAB: M01_Lab1_API_Basics.ipynb]
GitHub: github.com/mdehghani86/DADS5250-GenAI/blob/main/labs/M01/M01_Lab1_API_Basics.ipynb


======================================================

VIDEO 5c: GAMIFICATION — Temperature Playground
------------------------------------------------------

[INTERACTIVE: Temperature gamification HTML]
Existing asset from GitHub (Persian repo)


======================================================

VIDEO 6: LAB 2 WALKTHROUGH (Screen Recording, ~12 min)
------------------------------------------------------

[LAB: M01_Lab2_Parameters_Tokens.ipynb]
GitHub: github.com/mdehghani86/DADS5250-GenAI/blob/main/labs/M01/M01_Lab2_Parameters_Tokens.ipynb


======================================================

VIDEO 7: "MODULE 1 WRAP-UP" (Closing, 2-3 min)
------------------------------------------------------

[ON CAMERA] CLOSING

Here is what you accomplished this week. You connected
to two of the most powerful AI models on the planet --
not through a chat window, but through code. You
controlled parameters. You saw how temperature changes
output. You counted tokens and estimated costs.

That might sound simple. But think about what it means.
You now have programmatic access to intelligence.
Everything else in this course builds on this
foundation.

Next week -- how do you communicate with these models
effectively? The answer is prompt engineering. And it
starts with a coffee order. See you in Module 2.


======================================================
VERIFIED REFERENCES:
- 900M weekly ChatGPT users — Sam Altman, TechCrunch Oct 2025
- 4M developers on OpenAI API — OpenAI Enterprise Report 2025
- GPT-4.1-mini $0.15/$0.60 per 1M tokens — openai.com/api/pricing
- Gemini Flash $0.08/$0.30 — ai.google.dev/pricing
======================================================
