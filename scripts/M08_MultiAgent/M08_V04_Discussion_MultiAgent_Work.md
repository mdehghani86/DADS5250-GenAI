======================================================
MODULE: M08 — Multi-Agent Systems (CrewAI & LangGraph)
VIDEO: Student Discussion — Building Multi-Agent Systems at Work
PARTICIPANTS: Student 1, Student 2, Prof. Dehghani
DURATION: 5-8 minutes
======================================================

SETUP: Two former DADS 5250 students who have used multi-agent architectures in their professional work join Prof. Dehghani for a conversation about the realities of building and deploying multi-agent systems. The discussion is informal, conversational, and focused on practical experience.

PROMPT 1: "Tell us what you are working on now and how multi-agent systems fit into it."
  -> Suggested talking points:
     - What industry or domain they work in
     - What problem they tried to solve with a single agent first
     - When and why they realized they needed multiple agents
  -> Follow-up: "What was the moment you knew a single agent was not enough?"

PROMPT 2: "Walk us through the architecture. How did you divide responsibilities between agents?"
  -> Suggested talking points:
     - How they decided which roles to create
     - Whether they used CrewAI, LangGraph, or a custom setup
     - How agents communicate -- shared state, message passing, or something else
     - How they handled failures -- what happens when one agent makes a mistake
  -> Follow-up: "If you could redesign the system from scratch, what would you change?"

PROMPT 3: "What was the hardest part of building a multi-agent system that nobody warned you about?"
  -> Suggested talking points:
     - Debugging across agents -- tracing where something went wrong
     - Cost management -- multiple agents means multiple LLM calls
     - Latency -- waiting for agents to finish before the next one starts
     - Getting agents to share context without losing important information
  -> Follow-up: "How did you solve it? Or are you still solving it?"

PROMPT 4: "What advice would you give a student in this course who is about to build their first multi-agent system?"
  -> Suggested talking points:
     - Start simple -- two agents, not ten
     - Get one agent working perfectly before adding more
     - Test agents individually before testing the system
     - Think about cost early -- every agent call is an API call
     - Do not over-engineer the coordination layer

PROMPT 5: "If you had to pick one thing from this course that made the biggest difference in your career so far, what would it be?"
  -> Suggested talking points:
     - A specific skill, framework, or mental model
     - Something they did not expect to use but ended up relying on

CLOSING: Prof. Dehghani wraps up.
  "This is why we teach this course with real tools and real projects. The problems you just heard about -- debugging across agents, managing cost, designing clean handoffs -- those are the problems you will face at work. And now you know what to expect. Thank you both for coming back and sharing your experience."

======================================================
DIGITAL MEDIA NOTES:
- Record in conversation-style setup: three chairs, informal arrangement, good audio
- Add lower-third name/title cards for each participant when they first speak
- Consider adding brief screen captures or diagrams when students describe their architectures
- Post-production: add chapter markers for each prompt so students can jump to topics of interest
======================================================
