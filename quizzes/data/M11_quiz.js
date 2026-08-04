window.QUIZ = {
  meta: {
    module: "M11",
    title: "Claude Agent SDK, Google ADK & Claude Code",
    subtitle: "DADS 5250 Generative AI in Practice"
  },
  questions: [
    {
      id: "m11-q1",
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "According to the module, one thing that makes the <strong>Claude Agent SDK</strong> different is that it ships with <strong>built-in tools</strong>. Which set of tools does it provide out of the box?",
      options: [
        {
          letter: "A",
          text: "<code>Read</code>, <code>Write</code>, <code>Bash</code>, and <code>WebSearch</code>",
          explanation: "Correct: the SDK comes with these ready-made tools so you do not have to implement file reads, writes, shell commands, or web search yourself."
        },
        {
          letter: "B",
          text: "A vector database, an embedding model, and a reranker",
          explanation: "This lists RAG components, not the SDK's built-in tools. The module names Read, Write, Bash, and WebSearch as the batteries-included tools; retrieval infrastructure is a separate concern the SDK does not bundle."
        },
        {
          letter: "C",
          text: "A drag-and-drop visual workflow builder",
          explanation: "The Claude Agent SDK is a code toolkit, not a no-code canvas. The module frames it as a platform with built-in tools like Read, Write, Bash, and WebSearch, not a visual builder."
        },
        {
          letter: "D",
          text: "Nothing built in; you must wire every tool from scratch like in 2024 frameworks",
          explanation: "This describes exactly the old framework approach the SDK replaces. The whole point of the SDK is that tools such as Read, Write, Bash, and WebSearch just work without you writing glue code."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m11-q2",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Practical insight",
      prompt: "The module contrasts a coding chatbot with <strong>Claude Code</strong> using the phrase <em>\"the difference between a spell checker and a co-author.\"</em> What capability makes Claude Code behave like a co-author rather than a chatbot?",
      options: [
        {
          letter: "A",
          text: "It has access to your whole codebase, so it traces dependencies across files and updates every caller when a signature changes",
          explanation: "Correct: because it reasons about the project as a whole rather than a single pasted snippet, it knows changing one function means updating its callers elsewhere."
        },
        {
          letter: "B",
          text: "It uses a larger model than a chatbot, so its single-file suggestions are simply more accurate",
          explanation: "The module does not attribute the difference to model size or to better single-file suggestions. The distinction is codebase-wide awareness: it sees your directory structure, tests, and dependencies, not just the file in front of it."
        },
        {
          letter: "C",
          text: "It generates text you copy and paste back into your editor, only faster",
          explanation: "Copy-paste of snippets is the 2024 file-by-file assistant workflow the module explicitly contrasts against. Claude Code writes files and runs commands itself, acting on a model of how the whole project connects."
        },
        {
          letter: "D",
          text: "It never asks permission, so it can refactor everything instantly without interruptions",
          explanation: "This is both wrong and unsafe by the module's account. Claude Code proposes changes and asks before writing files or running commands; the co-author quality comes from full-project understanding, not from acting without approval."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m11-q3",
      difficulty: "medium",
      type: "tf",
      typeLabel: "True / False",
      prompt: "In Claude Code's <strong>trust model</strong>, the tool executes its proposed edits and commands automatically by default, and you only review actions afterward if something looks wrong.",
      correctAnswer: false,
      explanation: "False. The module describes a propose-review-approve-execute flow where every action goes through a permission step: Claude Code shows the file it wants to edit or the command it wants to run, and nothing happens without your explicit consent, with the default set to conservative (ask before everything). The common misconception is to picture an autonomous agent that acts first and reports later, but the design deliberately keeps you in control up front, letting you relax trust levels only as you build confidence."
    },
    {
      id: "m11-q4",
      difficulty: "medium",
      type: "multi",
      typeLabel: "Multiple select",
      prompt: "Based on the module's comparison of agent tooling, which statements are <strong>accurate</strong>? <em>Select all that apply.</em>",
      options: [
        {
          letter: "A",
          text: "Google ADK takes a code-first approach with native multi-agent orchestration and flexible deployment (local, Cloud Run, or Vertex AI)",
          explanation: "Correct: the module describes ADK as code-first, built around the Agent class, with native multi-agent support and the same code deployable across local, Cloud Run, and Vertex AI."
        },
        {
          letter: "B",
          text: "For most new projects, starting with the first-party SDK for your chosen model is the pragmatic default",
          explanation: "Correct: the module's honest recommendation is to start with the first-party SDK and reach for a framework only when the SDK cannot handle your orchestration needs."
        },
        {
          letter: "C",
          text: "First-party SDKs made LangChain, CrewAI, and LangGraph obsolete, so no one should use them anymore",
          explanation: "This overstates the module's point. It explicitly says those frameworks are not dead and still serve different purposes such as complex stateful workflows or role-based simulation; the SDK is just the pragmatic default for new projects."
        },
        {
          letter: "D",
          text: "The Claude Agent SDK handles multiple agents through a graph-based state machine, the same mechanism CrewAI uses",
          explanation: "This mixes up the models. The Claude Agent SDK orchestrates via subagents under a main orchestrator, LangGraph is the graph-based option, and CrewAI uses a role-based crew model, so the mechanisms are not the same."
        }
      ],
      correctIndices: [0, 1],
      explanation: "The module presents ADK as code-first with native multi-agent support and flexible deployment, and recommends first-party SDKs as the sensible default while noting frameworks like LangGraph and CrewAI still have their place."
    },
    {
      id: "m11-q5",
      difficulty: "hard",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "The Claude Agent SDK distinguishes <strong>Tools</strong> from <strong>Skills</strong>, and also supports <strong>subagents</strong>. Which mapping matches the module's mental model?",
      options: [
        {
          letter: "A",
          text: "Tools are atomic actions (like functions); Skills are higher-level reusable instruction sets (like libraries); subagents are specialized agents that work under a main orchestrator",
          explanation: "Correct: the module frames tools as atomic actions, skills as reusable higher-level capabilities, and subagents as specialists the orchestrator delegates to and collects results from."
        },
        {
          letter: "B",
          text: "Tools are reusable instruction sets, while Skills are the single atomic actions the agent calls one at a time",
          explanation: "This reverses the two definitions. In the module, tools are the atomic actions (functions) and skills are the higher-level reusable instruction sets (libraries), not the other way around."
        },
        {
          letter: "C",
          text: "Skills and subagents are the same thing: both are just alternative names for a single tool call",
          explanation: "The module treats them as distinct. Skills are higher-level capabilities the agent invokes, while subagents are separate specialized agents with their own tools and instructions running under an orchestrator, so collapsing them into one tool call is wrong."
        },
        {
          letter: "D",
          text: "Subagents replace the main agent entirely, so there is no orchestrator once you add them",
          explanation: "This misreads the design. Subagents work under a main orchestrator that delegates tasks and collects their results; the orchestrator remains in charge rather than being replaced."
        }
      ],
      correctIndex: 0
    }
  ]
};
