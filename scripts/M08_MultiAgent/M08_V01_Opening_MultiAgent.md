======================================================
MODULE: M08 — Multi-Agent Systems (CrewAI & LangGraph)
VIDEO: Opening — From Solo to Team
NARRATOR: Prof. Dehghani
DURATION: 4 minutes (~500 words)
======================================================

PART 1: OPENING HOOK
------------------------

I run a company called TwinAI.

When we started, I did everything. Sales. Engineering. Marketing. Customer support. I was the entire company in one person. And it worked -- for about three months.

Then it stopped working. I could not write code and answer customer emails at the same time. I could not design the product and close deals in the same week. It does not scale.

The moment I hired specialists and gave each one a clear role, everything changed. The engineer focused on engineering. The designer focused on design. I gave them context, set the direction, and let them do what they do best.

Multi-agent systems work the same way.

One agent cannot do everything well. It loses focus. It makes mistakes when the task gets too complex. But a team of specialized agents, each with a clear role, communicating with each other -- that is how you build systems that actually work at scale.

[ANIMATION: Single person juggling many tasks (dropping some) -> transition to a team of specialists, each handling one task cleanly]

PART 2: TWO APPROACHES TO MULTI-AGENT
------------------------

There are two major frameworks for building multi-agent systems, and they think about the problem differently.

CrewAI uses a role-based model. You define agents by their role -- researcher, writer, reviewer, manager. You assign each agent a goal and a set of tools. Then you define tasks and let the crew execute them. It feels like hiring a team. You describe who does what and CrewAI handles the coordination.

LangGraph uses a graph-based model. You define nodes -- each node is an agent or a function. You draw edges between them -- these are the transitions. You control exactly when and how data flows from one agent to another. It feels like designing a workflow. You draw the blueprint.

When do you use which? CrewAI when the problem is naturally role-based. Research teams. Content pipelines. Review workflows. LangGraph when you need precise control over the flow. Conditional branching. Loops. Human-in-the-loop checkpoints.

[ANIMATION: Left side: CrewAI diagram showing agents with role labels connected by task arrows. Right side: LangGraph diagram showing nodes and directed edges with conditional branches]

PART 3: REAL-WORLD EXAMPLES
------------------------

Customer support at scale. One agent reads the ticket. Another classifies the urgency. A third drafts the response. A fourth checks it for policy compliance. Each agent is simple. The system is powerful.

Research pipelines. One agent searches academic papers. Another summarizes findings. A third identifies contradictions. A fourth writes the synthesis. Companies like Cognition and Factory are building entire engineering teams out of multi-agent systems.

McKinsey estimates that 60 percent of enterprise AI deployments in 2026 involve some form of multi-agent architecture.

[ANIMATION: Customer support pipeline with four agent icons in sequence, each labeled with its role]

PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

If you can build a single agent, you are useful. If you can architect a multi-agent system, you are dangerous -- in the best way. You are the person who designs the team, not just the individual.

PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will build a CrewAI crew with specialized agents that collaborate on a research task. Then you will build a LangGraph workflow with conditional routing and state management.

By Friday, you will think about AI problems differently. Not "what can one model do?" but "what can a team of models accomplish together?"

Let us build the team.

======================================================
DIGITAL MEDIA NOTES:
- Opening animation: solo founder overwhelmed, then team forming -- parallels to single agent vs multi-agent
- Framework comparison: side-by-side animated diagrams of CrewAI (roles) vs LangGraph (graph), keep them on screen for 15+ seconds
- Customer support pipeline: animate data flowing through four agent nodes, with labels appearing as each agent processes
- Embedded poll: "Which sounds more natural to you?" (Role-based teams / Graph-based workflows / Not sure yet)
======================================================
