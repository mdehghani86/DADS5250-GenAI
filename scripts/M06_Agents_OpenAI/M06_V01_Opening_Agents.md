======================================================
MODULE: M06 — AI Agents & OpenAI Agents SDK
VIDEO: Opening — AI Agents
NARRATOR: Prof. Mohammad Dehghani
DURATION: 4-5 minutes (~540 words)
======================================================

PART 1: OPENING HOOK
------------------------

I play chess occasionally. Not well — but enough to know the difference between a beginner and an experienced player.

A new player reacts move by move. They see a threat. They block it. They see an opening. They take it. No plan. Just reflexes.

An experienced player thinks five or six moves ahead. They have a strategy. They plan contingencies. They adapt when the opponent does something unexpected. They reason about the board.

That is exactly the difference between a chain and an agent.

A chain follows a script. Step one, step two, step three. Done. An agent looks at the situation, decides what to do, uses tools, evaluates the result, and figures out its next move. It reasons. It plans. It adapts.

This is where AI gets genuinely powerful.

[ANIMATION: Split screen — left side shows a rigid chain diagram (linear arrows, step 1-2-3); right side shows an agent loop with branching paths, tool calls, and decision nodes]


PART 2: WHAT IS AN AGENT?
------------------------

An agent is a system where a language model controls the workflow.

In everything you have built so far, you controlled the flow. You decided what prompt to send. You decided what to do with the output. The model was a tool in your pipeline.

With an agent, the model is the decision-maker. You give it a goal, a set of tools, and instructions. It decides which tools to call, in what order, and when it has enough information to answer.

This works through something called the ReAct loop — Reason plus Act. The model thinks about what it needs. It takes an action — like calling a tool or looking up information. It observes the result. Then it reasons again. Think, act, observe. Repeat until the task is done.

The tools can be anything. A web search. A database query. A calculator. An API call. A code execution environment. The model picks the right tool for the job.

[ANIMATION: ReAct loop diagram — circular flow: Reason (thought bubble), Act (tool icon), Observe (magnifying glass), with arrows cycling back to Reason]


PART 3: THE 2026 LANDSCAPE SHIFT
------------------------

Here is what makes this module timely.

In 2024, building an agent meant picking a framework — LangChain, LangGraph, AutoGen — defining tools by hand, writing glue code, and debugging complex abstractions. It worked, but it was heavy.

In 2026, the landscape shifted. The model providers started shipping their own agent SDKs. Batteries included.

OpenAI released the Agents SDK. Anthropic released the Claude Agent SDK. Google released the Agent Development Kit. These are not frameworks built on top of APIs. They are native SDKs from the companies that build the models.

The OpenAI Agents SDK gives you agents with built-in tool calling, handoffs between agents, guardrails for safety, and tracing for debugging. You import the SDK, define your agent, give it tools, and run it. The plumbing is handled.

This is a real shift. Less boilerplate. More building.

[ANIMATION: Timeline — 2024: framework logos stacked with "glue code" labels; 2026: three SDK logos (OpenAI, Anthropic, Google) with "batteries included" label]


PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

Agents are where the industry is heading. Every major tech company is investing in agentic AI. The engineers who know how to build, test, and deploy agents are in extraordinary demand.

This is not a nice-to-have skill. This is the skill.


PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will build agents using the OpenAI Agents SDK. You will define tools. You will set up handoffs — where one agent passes a task to another. You will add guardrails. And you will use tracing to see exactly how your agent reasons through a problem.

By the end of this module, your AI will not just follow instructions. It will make decisions.

Let us build an agent.

======================================================
DIGITAL MEDIA NOTES:
- The chess analogy is strong — consider a quick visual of a chess board with thought lines projecting future moves
- The ReAct loop should be the signature diagram — animate it cycling 2-3 times
- The 2024 vs 2026 timeline is a key visual — make it feel like a real industry shift
- Consider embedding a 1-question poll: "Have you used an AI tool that felt like it was 'thinking' on its own?"
- End card: "Next: Lab — Building Agents with OpenAI Agents SDK"
======================================================
