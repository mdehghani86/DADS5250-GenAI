# M01: Getting Started with LLM APIs — Narrative Arc

## Key Message
"The chat window is the demo. The API is the product."

## Student Journey
- **Start**: "I use ChatGPT sometimes"
- **End**: "I can write code that talks to AI models, control their behavior, and understand what I'm paying for"

## Narrative Flow

### ACT 1: THE HOOK (Video 1, 3-4 min)

**Purpose**: Create urgency. Why should I care about APIs?

**Emotional beat**: "Wow, I had no idea there was something behind the chat window"

**Section flow**:
1. The Spark opening (Steve Jobs style / Personal Story / Provocative Question — pick one)
2. Key message delivered clearly: "The chat window is the demo. The API is the product."
3. Brief preview of what they will build this week — a working AI-powered program
4. Transition to Video 2: "But first, let us understand what we are connecting to."

**Connection to next**: The hook creates the "why" — Video 2 provides the "what."

---

### ACT 2: THE FOUNDATION (Video 2, 6-8 min)

**Purpose**: Build understanding. What are LLMs? How do they work?

**Emotional beat**: "Oh, so that is how it works under the hood"

**Section flow**:

1. **What is an LLM — the simplest explanation**
   - Two analogy options: the well-read colleague who has read everything but experienced nothing, or the world's best autocomplete
   - Key insight: LLMs predict the next word, they do not "think" or "understand"
   - Why this matters: explains hallucination, temperature, and limitations

2. **The three major models — GPT, Gemini, Claude**
   - Brief landscape: who makes what, what each is known for
   - Not a feature comparison — just enough for context
   - "We will primarily use GPT-4.1-mini and Gemini Flash in this course"

3. **Platform vs API — the two ways to access**
   - Platform = restaurant (you sit down, they serve you, their menu, their pace)
   - API = delivery service (you order what you want, when you want, in your own kitchen)
   - Key distinction: the platform is for consumers, the API is for builders

4. **How text generation actually works**
   - Token prediction, not thinking
   - Temperature = randomness dial
   - Tokens = the unit of text (roughly 0.75 words per token)
   - "Autocomplete on steroids" — powerful but not magical

5. **Why this matters for what you will build**
   - Hallucination comes from prediction, not malice
   - Temperature control matters for reliability
   - Token awareness matters for cost
   - Understanding the mechanism makes you a better builder

**Each section CONNECTS to the next**:
- 1 to 2: "Now you know what an LLM is. But which ones exist, and which will we use?"
- 2 to 3: "You have been using these models through the platform. But there is another way."
- 3 to 4: "So the API sends text to the model. But what does the model actually do with it?"
- 4 to 5: "Now you understand the mechanism. Here is why that understanding matters."

**Connection to next**: "You understand what an LLM is and how it generates text. Now let us talk about how you actually connect to one through code. That is what an API does."

---

### ACT 3: THE KEY CONCEPT (Video 3, 5-6 min)

**Purpose**: Teach the core skill. What is an API? How does it work?

**Emotional beat**: "That is actually not complicated at all"

**Section flow**:

1. **API from zero — what does A-P-I stand for?**
   - Application Programming Interface
   - Analogy: waiter in a restaurant (you give your order, the waiter takes it to the kitchen, brings back your food — you never enter the kitchen)
   - Three parts: request (your order), processing (the kitchen), response (your food)

2. **How an LLM API specifically works**
   - You send a message (the prompt)
   - The server processes it (the model generates a response)
   - You get back a structured response (JSON with the text, usage info, and metadata)
   - Every call costs money — you pay per token

3. **The actual code — 7 lines**
   - Walk through each line: import, client, request, model, messages, print
   - "That is the entire program. Seven lines."
   - Run it live — show the response
   - Break down the response object: choices, message, content, usage

4. **What this enables — the leap from consumer to builder**
   - Loops: process 1,000 documents automatically
   - Integration: connect AI to your own applications
   - Control: set temperature, system prompts, output format
   - Scale: what takes you 10 minutes in ChatGPT takes 2 seconds via API

**Connection to next**: "Before you can run this code, you need API keys. Your TA will walk you through that setup."

---

### ACT 4: THE SETUP (Video 4, TA, 5-7 min)

**Purpose**: Remove friction. Get everyone's environment working.

**Emotional beat**: "OK, I am set up and ready to go"

**TA covers (not scripted word-for-word)**:
1. OpenAI API key: platform.openai.com, billing, create key
2. Google Gemini key: aistudio.google.com, free tier
3. Colab Secrets: how to store keys securely (never hardcode)
4. Test cell: run a simple API call to verify both keys work
5. Common troubleshooting: billing not set up, key not saved, wrong secret name

**Critical placement**: This MUST come before Labs (Videos 5-6). Students cannot do the labs without working keys.

**Connection to next**: "Your environment is set up. Now open Lab 1 and let us make your first API call from code."

---

### ACT 5: THE PRACTICE (Videos 5-6, Labs, 20-24 min)

**Purpose**: Hands-on. Do it yourself.

**Emotional beat**: "I did it! I made an API call from code!"

**Lab 1 (Video 5, 10-12 min): First API Calls**
- First call to GPT-4.1-mini — the "hello world" of LLM APIs
- Response anatomy: what comes back, how to parse it
- System prompts: controlling the AI's personality
- Multi-turn conversation: maintaining context
- Exercise: Build a simple customer support bot (5-turn conversation)

**Lab 2 (Video 6, 10-12 min): Temperature, Tokens, Cost**
- Temperature experiments: same prompt at 0.0 vs 0.5 vs 1.0
- Tokenization: how text becomes tokens, why it matters
- Token counting: measuring input + output tokens
- Cost estimation: calculating the price of 1,000 API calls
- Exercise: Build a cost estimator function

**Alignment check**:
- Lab 1 covers: API calls (V3), response object (V3), multi-turn (V2-platform vs API concept)
- Lab 2 covers: temperature (V2-S4), tokens (V2-S4), cost (V3-S2)
- Both labs require: working API keys (V4)

**Connection to next**: The last cell of Lab 2 previews prompt engineering: "Notice how changing the system prompt changed the output completely? Next week, we go deep on that skill."

---

### ACT 6: THE CLOSE (Video 7, 2-3 min)

**Purpose**: Cement the learning. Bridge to M02.

**Emotional beat**: "I get it. And I want to learn more."

**Section flow**:

1. **Recap what they built**
   - You made your first API call
   - You parsed a response object
   - You built a multi-turn conversation
   - You controlled temperature and estimated cost
   - "You are no longer just a user of AI. You are a builder."

2. **The bridge to M02**
   - "You now know how to talk to the model through code. But here is the thing — the quality of what comes back depends entirely on what you send in."
   - "Next week: Prompt Engineering. How to write prompts that get exactly what you need, every time."
   - Coffee order callback (if used in M02 opening): "Think of it like ordering coffee..."

3. **Motivational close**
   - "Most people will never write a single line of code that talks to an AI model. You just did. That puts you ahead."

---

## Connections Checklist

| Check | Status |
|-------|--------|
| Does Lab 1 cover what Video 2-3 explain? | Yes — API calls, response object, multi-turn |
| Does Lab 2 cover temperature/tokens from Video 2? | Yes — temperature experiments, tokenization, cost |
| Does the TA video (V4) come BEFORE the labs? | Yes — setup before practice |
| Does the closing tease M02 naturally? | Yes — "coffee order" = prompt engineering |
| Is the key message reinforced in both opening and closing? | Yes — "The chat window is the demo. The API is the product." |
| Are all facts verifiable? | Must verify: ChatGPT user stats, Google code stat, token pricing |
| Are personal stories marked as placeholders? | Yes — [YOUR STORY] tags where needed |

## Duration Budget

| Video | Duration | Cumulative |
|-------|----------|------------|
| V1: Opening / Hook | 3-4 min | 3-4 min |
| V2: Foundation (LLMs) | 6-8 min | 9-12 min |
| V3: Key Concept (APIs) | 5-6 min | 14-18 min |
| V4: TA Setup | 5-7 min | 19-25 min |
| V5: Lab 1 | 10-12 min | 29-37 min |
| V6: Lab 2 | 10-12 min | 39-49 min |
| V7: Closing | 2-3 min | 41-52 min |

**Total**: ~41-52 minutes of video content per module (typical for an online graduate course module)
