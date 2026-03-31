======================================================
MODULE: M02 — Prompt Engineering
VIDEO: Student Discussion — How I Use Prompt Engineering Every Day
PARTICIPANTS: Alex (former student, now data analyst), Priya (former student, now ML engineer), Prof. Dehghani
DURATION: 6-7 minutes
======================================================

SETUP: Two former DADS 5250 students join Prof. Dehghani to discuss how prompt engineering shows up in their daily work. The conversation is relaxed and candid — real experiences, real mistakes, real advice. Filmed in a casual setting, three chairs, no slides.

PROMPT 1: "When did prompt engineering click for you?"
  -> Suggested talking points:
     - The moment they realized vague prompts were the problem, not the model
     - A specific task where rewriting the prompt changed everything
     - The difference between "playing with ChatGPT" and engineering a prompt for a production system
  -> Follow-up: "Was there a before-and-after moment where you saw the output quality jump?"

PROMPT 2: "Walk us through how you actually use prompting at work."
  -> Suggested talking points:
     - Alex: uses system messages to enforce consistent report formatting across dozens of API calls daily; the role definition alone cut revision time in half
     - Priya: builds few-shot examples into pipelines so the model matches the team's existing data labeling conventions; chain-of-thought for debugging logic in generated code
     - How they organize and version their prompts (prompt libraries, template files, shared docs)
  -> Follow-up: "Do you treat prompts like code — with version control, testing, iteration?"

PROMPT 3: "What is the worst prompting mistake you have made?"
  -> Suggested talking points:
     - Forgetting to specify output format and getting prose when they needed JSON
     - A prompt that worked perfectly in testing but failed on edge cases in production
     - Assuming the model "knew" context that was never actually provided
     - Spending hours debugging code when the real problem was a poorly written prompt
  -> Follow-up: "How did you catch it, and what did you change?"

PROMPT 4: "What would you tell a student just starting with prompt engineering?"
  -> Suggested talking points:
     - Start with the four elements: role, task, context, format — every single time
     - Test your prompts with adversarial inputs, not just the happy path
     - Read your prompts out loud — if a human would be confused, the model will be too
     - Do not over-engineer on the first try; iterate, test, refine
     - The skill compounds — the more you practice, the faster you get

PROMPT 5 (Prof. Dehghani): "How has prompting changed how you think about communicating in general?"
  -> Suggested talking points:
     - Being more precise in emails, Slack messages, meeting agendas
     - Realizing that clear instructions benefit humans and machines equally
     - The meta-skill: prompt engineering teaches you to think about what you actually want before you ask for it

CLOSING: Prof. Dehghani wraps up.
  "What I love about this conversation is that neither of you talked about prompt engineering as a trick or a hack. You talked about it as a discipline. Clarity, structure, iteration. Those are engineering principles. And they apply whether you are talking to a model or talking to a team. Thank you both for sharing this."

======================================================
DIGITAL MEDIA NOTES:
- Film in a casual three-person setup — no podium, no slides, conversational feel
- Use lower-third name cards: "Alex — Data Analyst, Class of 2025" / "Priya — ML Engineer, Class of 2025"
- Consider inserting brief screen captures or code snippets when participants describe specific prompting examples (e.g., showing a before/after prompt side by side)
- Post-production: add subtle chapter markers for each prompt topic so students can navigate
- Optional: pull 2-3 short clips (15-30 sec) as standalone social media or Canvas announcement teasers
======================================================
