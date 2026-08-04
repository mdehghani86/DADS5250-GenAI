window.QUIZ = {
  "meta": {
    "module": "M08",
    "title": "Multi-Agent Systems (CrewAI)",
    "subtitle": "DADS 5250 Generative AI in Practice"
  },
  "questions": [
    {
      "id": "m08-q1",
      "difficulty": "easy",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "In this module, what are the <strong>three core building blocks</strong> of CrewAI?",
      "options": [
        {
          "letter": "A",
          "text": "Agents, Tasks, and Crews",
          "explanation": "Correct: an agent is a specialist, a task is an assignment, and a crew is the team that runs the agents and tasks together."
        },
        {
          "letter": "B",
          "text": "Nodes, Edges, and Graphs",
          "explanation": "This describes LangGraph, not CrewAI. The module explicitly contrasts them: with LangGraph you build the graph yourself, while CrewAI raises the abstraction so you think in agents, tasks, and crews instead of nodes and edges."
        },
        {
          "letter": "C",
          "text": "Prompts, Chains, and Retrievers",
          "explanation": "These are LangChain and RAG concepts from earlier modules, not CrewAI's building blocks. CrewAI's abstraction is organizational -- agents with roles, tasks with expected outputs, and a crew that orchestrates them."
        },
        {
          "letter": "D",
          "text": "Roles, Goals, and Backstories",
          "explanation": "These three are the fields that define a single agent, not the framework's top-level building blocks. The three building blocks are Agents, Tasks, and Crews; role, goal, and backstory sit inside the Agent."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m08-q2",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Practical insight",
      "prompt": "According to the module, why does a <strong>single agent</strong> struggle when asked to research a topic, write a report, and then fact-check it all on its own?",
      "options": [
        {
          "letter": "A",
          "text": "It has one context window and one persona, so it loses track of which role it is playing and quality degrades",
          "explanation": "Correct: the module frames this as an architecture problem -- one agent juggling many roles fills its context and gets confused, which is why specialization into a team helps."
        },
        {
          "letter": "B",
          "text": "The underlying model is simply not smart enough, so you need a more powerful LLM",
          "explanation": "The module says the opposite: this is not a model problem, it is an architecture problem. Swapping in a smarter model does not fix role confusion; splitting the work across specialized agents does."
        },
        {
          "letter": "C",
          "text": "A single agent cannot call any tools, so it has no way to gather information",
          "explanation": "Single agents can use tools -- that was covered in the agents module. The single-agent limitation here is about losing context and mixing up roles across a long multi-step job, not an inability to use tools."
        },
        {
          "letter": "D",
          "text": "CrewAI forbids one agent from being assigned more than one task",
          "explanation": "There is no such rule in CrewAI. The point is a design principle about specialization: a narrow, clear role produces better quality than one agent trying to be researcher, writer, and editor at once."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m08-q3",
      "difficulty": "medium",
      "type": "order",
      "typeLabel": "Ordering",
      "prompt": "Put the steps of building and running a basic <strong>sequential</strong> CrewAI crew (as shown in the module's code) into the correct order, from first to last.",
      "items": [
        "Assemble the Crew with its agents, tasks, and process",
        "Define the agents, each with a role, goal, and backstory",
        "Call crew.kickoff() to run the pipeline",
        "Define the tasks, each with a description, expected output, and assigned agent"
      ],
      "correctOrder": [
        2,
        0,
        3,
        1
      ],
      "explanation": "The correct sequence is: define the agents (role, goal, backstory), then define the tasks (description, expected output, assigned agent), then assemble the Crew listing those agents and tasks with a process, then call crew.kickoff() to run it. Agents and tasks must exist before a crew can reference them, and kickoff runs last."
    },
    {
      "id": "m08-q4",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "In the module, what is the key difference between the <strong>sequential</strong> and <strong>hierarchical</strong> crew processes?",
      "options": [
        {
          "letter": "A",
          "text": "Sequential runs tasks in a fixed order; hierarchical adds a manager agent that delegates work and can send it back for revision",
          "explanation": "Correct: sequential is a predictable production line, while hierarchical uses a manager agent to decide who works next and review or reassign the output."
        },
        {
          "letter": "B",
          "text": "Sequential uses one agent; hierarchical uses many agents",
          "explanation": "Both processes can use many agents. The difference is orchestration, not agent count: sequential passes work in a fixed order, whereas hierarchical adds a manager that dynamically delegates among the agents."
        },
        {
          "letter": "C",
          "text": "Sequential agents cannot share context; hierarchical agents can",
          "explanation": "Context sharing happens in both -- each task's output flows to downstream tasks in a sequential crew too. The real distinction is that hierarchical introduces a manager agent that controls task order dynamically."
        },
        {
          "letter": "D",
          "text": "Sequential is only for research tasks; hierarchical is only for writing tasks",
          "explanation": "Neither process is tied to a task type. The module frames the choice around structure: sequential for predictable linear flows, hierarchical when task order is dynamic and needs a manager to coordinate."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": 5,
      "difficulty": "hard",
      "type": "mc",
      "typeLabel": "Coding",
      "prompt": "In CrewAI, what is the correct way to assemble and run a crew in code?",
      "code": "crew = Crew(agents=[researcher, writer], tasks=[t1, t2], process=Process.sequential)\nresult = crew.kickoff()",
      "options": [
        {
          "letter": "A",
          "text": "Define the Agents and Tasks, pass them to Crew(agents=[...], tasks=[...], process=...), then call crew.kickoff().",
          "explanation": "Correct: build the specialists and their tasks, form the crew, then kick it off."
        },
        {
          "letter": "B",
          "text": "Call each agent.run() by hand and stitch the outputs together; a Crew is unnecessary.",
          "explanation": "CrewAI's value is the Crew orchestrating agents and tasks; running agents by hand throws that away."
        },
        {
          "letter": "C",
          "text": "Create the Crew first, then define the agents and tasks afterward.",
          "explanation": "Agents and tasks must exist before the Crew can reference them, so they are defined first."
        },
        {
          "letter": "D",
          "text": "Call crew.train() to fine-tune a model before the crew can run.",
          "explanation": "kickoff() runs the crew with existing models; there is no required training step."
        }
      ],
      "correctIndex": 0
    }
  ]
};
