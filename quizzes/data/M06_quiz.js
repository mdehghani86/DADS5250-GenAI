window.QUIZ = {
  meta: {
    module: "M06",
    title: "AI Agents: Concepts & LangGraph",
    subtitle: "DADS 5250 Generative AI in Practice"
  },
  questions: [
    {
      id: "m06-q1",
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "According to the module, what is the fundamental difference between a <strong>chain</strong> and an <strong>agent</strong>?",
      options: [
        {
          letter: "A",
          text: "A chain follows a fixed sequence of steps every time, while an agent reasons at runtime and decides what to do next.",
          explanation: "Correct: the module frames a chain as a script that runs the same path every time and an agent as a decision-maker that picks its path dynamically."
        },
        {
          letter: "B",
          text: "A chain can call tools but an agent cannot call any tools.",
          explanation: "This reverses the roles: it is the agent that reasons about and calls tools in a loop. Chains run a fixed pipeline, while tool-using decision-making is exactly what defines an agent."
        },
        {
          letter: "C",
          text: "A chain uses an LLM but an agent never uses an LLM.",
          explanation: "This misunderstands agents: an agent is built on an LLM that reasons plus tools plus a loop. The LLM is the reasoning engine of the agent, not something agents avoid."
        },
        {
          letter: "D",
          text: "A chain is always slower and less predictable than an agent.",
          explanation: "This inverts their properties: chains are described as predictable and efficient, while agents are flexible but less predictable. Chains take the same path each run, so they are the predictable option."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m06-q2",
      difficulty: "medium",
      type: "multi",
      typeLabel: "Multiple select",
      prompt: "The module names <strong>three ingredients</strong> that make something an agent. Which of the following are those ingredients? <em>(Select all that apply.)</em>",
      options: [
        {
          letter: "A",
          text: "An LLM that can reason about the situation",
          explanation: "Correct: the reasoning LLM is the first ingredient, deciding what information is needed at each step."
        },
        {
          letter: "B",
          text: "Tools it can reach for (functions it can call)",
          explanation: "Correct: tools are functions the agent can call, such as search or calculate, chosen at runtime."
        },
        {
          letter: "C",
          text: "A loop that lets it keep going until the job is done",
          explanation: "Correct: the loop is what turns single function calls into a repeating Reason-Act-Observe cycle until the task is complete."
        },
        {
          letter: "D",
          text: "A fixed pipeline defined in advance by the developer",
          explanation: "This describes a chain, not an agent. A fixed, predefined pipeline is the opposite of an agent, whose whole point is deciding the path at runtime rather than following preset steps."
        }
      ],
      correctIndices: [0, 1, 2],
      explanation: "The three ingredients are a reasoning LLM, tools it can call, and a loop that continues until the task is done. A fixed pipeline is a chain, which is precisely what an agent is contrasted against."
    },
    {
      id: "m06-q3",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Graphic based",
      prompt: "The diagram shows the core loop that powers every modern agent. What is the correct name and order of its stages?",
      diagram: "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg'><rect x='40' y='95' width='130' height='50' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='105' y='125' text-anchor='middle' font-family='sans-serif' font-size='15' fill='#1e293b' font-weight='600'>Reason</text><rect x='245' y='95' width='130' height='50' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='310' y='125' text-anchor='middle' font-family='sans-serif' font-size='15' fill='#1e293b' font-weight='600'>Act</text><rect x='450' y='95' width='130' height='50' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='515' y='125' text-anchor='middle' font-family='sans-serif' font-size='15' fill='#1e293b' font-weight='600'>Observe</text><line x1='170' y1='120' x2='240' y2='120' stroke='#2563EB' stroke-width='2' marker-end='url(#a)'/><line x1='375' y1='120' x2='445' y2='120' stroke='#2563EB' stroke-width='2' marker-end='url(#a)'/><path d='M 515 145 Q 515 200 310 200 Q 105 200 105 145' fill='none' stroke='#64748b' stroke-width='2' stroke-dasharray='5,4' marker-end='url(#a)'/><text x='310' y='225' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#64748b'>Repeat until task is complete</text><defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M 0 0 L 10 5 L 0 10 z' fill='#2563EB'/></marker></defs></svg>",
      options: [
        {
          letter: "A",
          text: "The ReAct loop: Reason, Act, Observe, then Repeat until the task is complete.",
          explanation: "Correct: the agent reasons about what it needs, acts by calling a tool, observes the result, and repeats until done."
        },
        {
          letter: "B",
          text: "The RAG loop: Retrieve, Augment, Generate.",
          explanation: "RAG is the retrieval pipeline from Module 5, not the agent loop. This diagram shows reasoning and tool use repeating, which is ReAct, not retrieval-augmented generation."
        },
        {
          letter: "C",
          text: "Observe, then Act, then Reason, executed exactly once with no repetition.",
          explanation: "This scrambles the order and drops the loop. The agent reasons first to decide what to fetch, and the dashed arrow shows it repeats rather than running a single one-shot pass."
        },
        {
          letter: "D",
          text: "A LangChain chain: Prompt, Model, Parser in a fixed line.",
          explanation: "That is a linear chain, which never loops back. The looping arrow here is the defining feature of an agent, so this fixed one-way pipeline does not match the diagram."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m06-q4",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "In LangGraph, what is the role of a <strong>conditional edge</strong>?",
      options: [
        {
          letter: "A",
          text: "A function that inspects the current state and returns the name of the next node to route to, enabling branching.",
          explanation: "Correct: a conditional edge is a small function that reads the state and returns which node runs next, which is where branching decisions happen."
        },
        {
          letter: "B",
          text: "A block of shared memory that flows through the entire graph.",
          explanation: "That describes state, not an edge. State is the shared memory carried between nodes, whereas a conditional edge is the decision function that chooses the next node based on that state."
        },
        {
          letter: "C",
          text: "A step that calls the LLM or executes a tool to update the data.",
          explanation: "That describes a node, not an edge. Nodes do the processing work, while conditional edges only decide which node the state moves to next."
        },
        {
          letter: "D",
          text: "The compile call that turns the graph into a runnable object.",
          explanation: "Compiling is the final build step, not an edge. A conditional edge is defined before compilation and governs runtime routing between nodes rather than producing the runnable graph."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m06-q5",
      difficulty: "hard",
      type: "mc",
      typeLabel: "Coding",
      prompt: "This snippet mimics a tiny <strong>ReAct-style</strong> agent choosing a tool based on the query, then looping until it is done. What does it print?",
      code: "def calculator(a, b):\n    return a + b\n\ndef search(q):\n    return \"result:\" + q\n\ntools = {\"add\": calculator, \"find\": search}\ntasks = [(\"add\", (2, 3)), (\"find\", (\"boston\",))]\nlog = []\nfor name, args in tasks:\n    obs = tools[name](*args)\n    log.append(str(obs))\nprint(\" | \".join(log))",
      options: [
        {
          letter: "A",
          text: "5 | result:boston",
          explanation: "Correct: calculator(2, 3) returns 5 and search('boston') returns 'result:boston', joined by ' | ' to print exactly: 5 | result:boston"
        },
        {
          letter: "B",
          text: "5 | resultboston",
          explanation: "This drops the colon, but search returns 'result:' + q, which keeps the colon. The concatenation produces 'result:boston', not 'resultboston'."
        },
        {
          letter: "C",
          text: "add | find",
          explanation: "This prints the tool names instead of their outputs. The loop appends the observation obs returned by each tool call, not the key name used to look the tool up."
        },
        {
          letter: "D",
          text: "23 | result:boston",
          explanation: "This treats (2, 3) as string concatenation, but they are integers, so calculator returns the sum 5, not '23'. Integer addition yields 5, giving '5 | result:boston'."
        }
      ],
      correctIndex: 0
    }
  ]
};
