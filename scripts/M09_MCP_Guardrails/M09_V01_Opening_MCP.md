======================================================
MODULE: M09 — MCP & Guardrails
VIDEO: Opening — The USB of AI
NARRATOR: Prof. Dehghani
DURATION: 4 minutes (~490 words)
======================================================

PART 1: OPENING HOOK
------------------------

Think about USB.

Before USB, every device had its own proprietary connector. Your printer had one cable. Your camera had a different one. Your keyboard, your mouse, your external drive -- all different. You opened a drawer and it was a graveyard of cables you could not tell apart.

Then USB came along. One standard. One connector. Plug anything into anything. Printers, cameras, phones, hard drives -- they all just worked.

MCP -- the Model Context Protocol -- is doing the same thing for AI.

One standard way for any AI model to connect to any tool. Any database. Any service. Before MCP, every integration was custom. You wanted your agent to read from a database? Write a custom tool. You wanted it to send an email? Write another custom tool. You wanted it to search your company's documents? Another custom tool. Every connection was bespoke.

MCP changed that. One protocol. Universal compatibility.

[ANIMATION: Drawer full of tangled proprietary cables -> transition to a single USB cable. Then: messy web of custom API integrations -> clean MCP connections radiating from a central model]

PART 2: HOW MCP WORKS
------------------------

Here is the architecture in plain English.

An MCP server is a small program that exposes a set of capabilities. It could be a Gmail server that lets AI read and send email. A database server that lets AI run queries. A file system server that lets AI read and write documents.

Your AI model connects to these servers through a standard protocol. It discovers what tools are available, understands their parameters, and calls them when needed. The model does not need custom code for each integration. It just speaks MCP.

This is why, in 2026, every major AI company adopted it. OpenAI, Google, and Anthropic all support MCP. It became the industry standard because the alternative -- custom integrations for every tool -- simply does not scale.

[ANIMATION: Diagram showing an AI model in the center connected to MCP servers: Gmail, Database, File System, Slack, Calendar -- each with a standardized MCP connection line]

PART 3: GUARDRAILS -- THE SAFETY LAYER
------------------------

But connectivity without control is dangerous.

If your agent can send emails, what stops it from sending a thousand? If it can run database queries, what stops it from deleting records? If it can access files, what stops it from reading sensitive documents?

Guardrails. Input validation. Output filtering. Rate limiting. Permission boundaries. You define what the agent can and cannot do, and the system enforces it before any action executes.

Nvidia reported that 78 percent of enterprises cite safety and guardrails as the top barrier to AI agent deployment. The companies that solve this problem ship. The ones that do not stay in the pilot phase forever.

[ANIMATION: Agent action flowing through a guardrails checkpoint -- green checkmark for approved actions, red X for blocked actions]

PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

Connecting AI to real systems is where the value is. Models that just answer questions are demos. Models that read your data, take actions, and respect boundaries -- those are products. If you understand MCP and guardrails, you can build the products.

PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will build an MCP server from scratch. You will connect an AI model to it. And you will implement guardrails that control what the agent is allowed to do.

You are about to give your agents hands. And teach them the rules.

======================================================
DIGITAL MEDIA NOTES:
- Opening animation: cable drawer chaos to USB simplicity -- make it visual and relatable
- MCP architecture diagram: keep it clean, show the protocol as a standard "bus" connecting model to multiple servers
- Guardrails checkpoint: animate an agent action being evaluated -- approved vs blocked, with a brief label showing why
- Consider an embedded 1-question quiz: "What problem does MCP solve?" (A: Universal AI-to-tool connectivity)
======================================================
