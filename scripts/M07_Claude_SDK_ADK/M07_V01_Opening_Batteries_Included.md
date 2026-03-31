======================================================
MODULE: M07 — Claude Agent SDK & Google ADK
VIDEO: Opening — Batteries Included
NARRATOR: Prof. Dehghani
DURATION: 4 minutes (~480 words)
======================================================

PART 1: OPENING HOOK
------------------------

Think about the first time you used a smartphone.

Before that, you needed a separate camera. A GPS device. An MP3 player. A calculator. And a phone. Five devices in your bag just to get through the day.

The smartphone did not invent any of those things. It just put them all in one device. And once it did, everything changed. You stopped carrying five things. You carried one.

That is what happened to AI agent building in 2026.

In 2024 and 2025, building an AI agent meant stitching together five or six libraries. A framework for orchestration. A separate tool for file access. Another for web search. Another for code execution. You spent more time wiring things together than actually building.

Claude Agent SDK and Google ADK changed that. They are the smartphones of agent development. Batteries included. Everything you need in one package.

[ANIMATION: Split screen -- left side shows a desk cluttered with separate devices (camera, GPS, phone, MP3 player); right side shows a single smartphone. Then transition: left side shows scattered Python libraries and imports; right side shows a single SDK import]

PART 2: THE SHIFT TO BATTERIES-INCLUDED
------------------------

Let me explain what "batteries included" actually means.

Claude Agent SDK ships with built-in tools. Read files. Write files. Run bash commands. Search the web. Grep through codebases. Your agent can do all of that out of the box. No plugins. No third-party wrappers. No configuration files.

Google ADK does the same thing from Google's side. Built-in search. Built-in code execution. Built-in memory. And both SDKs introduced something powerful: the concept of skills versus tools. A tool is a single action. A skill is a reusable capability -- a bundle of tools and instructions that the agent can invoke when it recognizes the right context.

This is the difference between handing someone a hammer and handing them a carpentry kit with instructions.

[ANIMATION: Diagram showing SDK architecture -- single import at top, branching into built-in tools (Read, Write, Bash, WebSearch, Grep) and Skills layer on top]

PART 3: REAL-WORLD IMPACT
------------------------

The numbers tell the story.

Companies that switched from custom framework stacks to these SDKs reported shipping agents ten times faster. What used to take a team two weeks -- setting up tool integrations, error handling, retry logic -- now comes out of the box in an afternoon.

Anthropic reported that Claude Agent SDK powered over 100,000 agent deployments within three months of its release. Google ADK became the default for enterprise teams already in the Google Cloud ecosystem.

[ANIMATION: Timeline graphic -- 2024: "Weeks to build an agent" vs 2026: "Hours to build an agent" with SDK logos]

PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

If you learned to build agents in the last two modules using OpenAI's SDK and LangGraph, you already understand the fundamentals. Now you are learning the tools that the industry actually deploys with. Claude Agent SDK and Google ADK are not academic exercises. They are production infrastructure.

PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will build agents with both SDKs. You will give them tools, define skills, and watch them reason through multi-step tasks without you writing the orchestration logic.

The frameworks did the heavy lifting for you before. Now the SDK does it.

Let us see what that looks like.

======================================================
DIGITAL MEDIA NOTES:
- Opening animation: physical devices morphing into smartphone, then transition to scattered library logos morphing into single SDK icon
- Architecture diagram: clean, minimal -- show the SDK as a single box with built-in tools radiating outward
- Consider a quick side-by-side code comparison: "Before (5 imports, 30 lines of setup)" vs "After (1 import, 5 lines)"
- Embedded poll: "Which SDK are you most interested in?" (Claude Agent SDK / Google ADK / Both)
======================================================
