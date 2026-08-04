window.QUIZ = {
  "meta": {
    "module": "M12",
    "title": "AI Platforms: Google A2A & OpenAI Agents SDK",
    "subtitle": "DADS 5250 Generative AI in Practice"
  },
  "questions": [
    {
      "id": "m12-q1",
      "difficulty": "easy",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "The module frames Google's <strong>A2A</strong> and the OpenAI Agents SDK as two <em>philosophies</em>. Which pairing does the module use to describe them?",
      "options": [
        {
          "letter": "A",
          "text": "Google thinks in open protocols; OpenAI thinks in an opinionated SDK",
          "explanation": "Correct: Google's A2A is an open standard so any agent can talk to any other, while the OpenAI Agents SDK is a small Python toolkit for building an agent app fast."
        },
        {
          "letter": "B",
          "text": "Google ships a Python SDK; OpenAI publishes an open wire protocol",
          "explanation": "This reverses the two companies. In the module, Google is the one publishing the open A2A protocol and OpenAI is the one shipping the opinionated Python SDK, not the other way around."
        },
        {
          "letter": "C",
          "text": "Both are open protocols governed by the Linux Foundation",
          "explanation": "Only A2A was donated to the Linux Foundation for vendor-neutral governance. The OpenAI Agents SDK is a Python framework, not a foundation-governed protocol, so calling both open protocols is wrong."
        },
        {
          "letter": "D",
          "text": "Both are closed, single-vendor products that cannot interoperate with other tools",
          "explanation": "A2A is explicitly an open spec anyone can implement, and the module stresses interoperability across frameworks. Describing them as closed and non-interoperable contradicts the whole point of the module."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m12-q2",
      "difficulty": "medium",
      "type": "multi",
      "typeLabel": "Multiple select",
      "prompt": "According to the module, which statements about a Google <strong>A2A Agent Card</strong> are true? <em>Select all that apply.</em>",
      "options": [
        {
          "letter": "A",
          "text": "It is a JSON document hosted at a well-known URL such as /.well-known/agent.json",
          "explanation": "Correct: the Agent Card is JSON published at a well-known endpoint so any caller can fetch it before sending work."
        },
        {
          "letter": "B",
          "text": "It advertises the agent's name, service URL, skills, and required authentication",
          "explanation": "Correct: those are exactly the fields the module lists, and a calling agent reads them to decide whether this is the right collaborator."
        },
        {
          "letter": "C",
          "text": "It is the actual unit of work one agent sends to another to be processed",
          "explanation": "This confuses the Agent Card with the Task. The Card is a description read during discovery; the Task is the separate structured request that carries the actual work to be done."
        },
        {
          "letter": "D",
          "text": "It must be written in a proprietary binary format that only Google tools can read",
          "explanation": "The module emphasizes A2A rides on boring, proven web tech and the Card is plain JSON any engineer can read. A proprietary binary format contradicts the open, interoperable design."
        }
      ],
      "correctIndices": [
        0,
        1
      ],
      "explanation": "An Agent Card is a JSON 'business card' at a well-known URL that advertises the agent's name, service URL, skills, and auth; the separate Task object carries the real work."
    },
    {
      "id": "m12-q3",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Graphic based",
      "prompt": "The diagram shows the OpenAI Agents SDK execution model. Based on the module, what is the role of the <strong>Runner</strong>?",
      "diagram": "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg' font-family='Outfit, sans-serif'><rect x='16' y='96' width='120' height='52' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='76' y='118' text-anchor='middle' font-size='13' fill='#1e293b' font-weight='600'>Runner</text><text x='76' y='136' text-anchor='middle' font-size='10' fill='#64748b'>run(agent, input)</text><line x1='136' y1='122' x2='210' y2='122' stroke='#64748b' stroke-width='1.5'/><rect x='210' y='96' width='150' height='52' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='285' y='118' text-anchor='middle' font-size='13' fill='#1e293b' font-weight='600'>Agent</text><text x='285' y='136' text-anchor='middle' font-size='10' fill='#64748b'>name + instructions</text><line x1='360' y1='110' x2='452' y2='44' stroke='#64748b' stroke-width='1.5'/><line x1='360' y1='122' x2='452' y2='122' stroke='#64748b' stroke-width='1.5'/><line x1='360' y1='134' x2='452' y2='200' stroke='#64748b' stroke-width='1.5'/><rect x='452' y='20' width='150' height='44' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='527' y='40' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>Tools</text><text x='527' y='55' text-anchor='middle' font-size='10' fill='#64748b'>@function_tool</text><rect x='452' y='100' width='150' height='44' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='527' y='120' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>Handoffs</text><text x='527' y='135' text-anchor='middle' font-size='10' fill='#64748b'>route to specialists</text><rect x='452' y='180' width='150' height='44' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='527' y='200' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>Guardrails</text><text x='527' y='215' text-anchor='middle' font-size='10' fill='#64748b'>input / output checks</text></svg>",
      "options": [
        {
          "letter": "A",
          "text": "It is the execution engine that takes an agent plus an input, drives the tool-calling and handoff loop, and returns the result",
          "explanation": "Correct: the Runner runs the agentic loop end to end so you call one method and read the answer from result.final_output."
        },
        {
          "letter": "B",
          "text": "It is the LLM prompt template that defines the agent's personality and instructions",
          "explanation": "Instructions live on the Agent, not the Runner. The Runner does not define the agent's job description; it executes the loop for whatever agent you hand it."
        },
        {
          "letter": "C",
          "text": "It is the decorator that turns a Python function into a callable tool",
          "explanation": "That decorator is @function_tool, a separate piece. The Runner is the execution engine that drives the loop, not the mechanism that registers tools."
        },
        {
          "letter": "D",
          "text": "It is the safety layer that blocks unsafe requests before the model runs",
          "explanation": "Blocking unsafe input is the job of guardrails, which fail fast before the model runs. The Runner executes the agentic loop; it is not the validation layer."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m12-q4",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "In the lab's support app, a <strong>Triage</strong> agent lists specialists in <code>handoffs=[...]</code> and routes each request. What makes the module call the handoff the SDK's signature idea?",
      "options": [
        {
          "letter": "A",
          "text": "Routing is decided at runtime: the triage agent reads each request and delegates to the right specialist, all inside one run",
          "explanation": "Correct: instead of hard-wiring every path, the triage agent picks the specialist dynamically per request while the Runner drives the single run."
        },
        {
          "letter": "B",
          "text": "It forces you to enumerate every possible request path in advance before running",
          "explanation": "That is the opposite of the module's point. Handoffs exist so you do NOT enumerate every path; routing is chosen at runtime based on the incoming request."
        },
        {
          "letter": "C",
          "text": "It spawns a brand-new Runner and event loop for each specialist agent",
          "explanation": "The whole exchange is one run driven by a single Runner call. Control moves between agents within that run; it does not start a new Runner or event loop per specialist."
        },
        {
          "letter": "D",
          "text": "It merges all specialists into one large do-everything agent for simplicity",
          "explanation": "The module warns that one giant do-everything agent gets brittle fast. Handoffs keep specialists small and separate, with triage routing between them, which is the reverse of merging them."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": 5,
      "difficulty": "hard",
      "type": "mc",
      "typeLabel": "Coding",
      "prompt": "In the OpenAI Agents SDK, what is the correct way to run an agent in code?",
      "code": "agent = Agent(name=\"Helper\", instructions=\"...\", tools=[get_weather])\nresult = await Runner.run(agent, \"What's the weather in Boston?\")\nprint(result.final_output)",
      "options": [
        {
          "letter": "A",
          "text": "Define an Agent with instructions and tools, then call Runner.run(agent, input); the Runner drives the tool and handoff loop and returns result.final_output.",
          "explanation": "Correct: you describe the agent and the Runner executes the whole agentic loop."
        },
        {
          "letter": "B",
          "text": "Manually loop over tool calls and append messages yourself, exactly like the raw Chat Completions API.",
          "explanation": "That is the boilerplate the SDK removes. The Runner handles the call-execute-return loop for you."
        },
        {
          "letter": "C",
          "text": "Agents run automatically as soon as they are imported, so no Runner call is needed.",
          "explanation": "Nothing runs until you invoke the Runner on an agent with an input."
        },
        {
          "letter": "D",
          "text": "Call Runner.train(agent) before the agent can answer.",
          "explanation": "There is no training step; Runner.run executes the agent immediately."
        }
      ],
      "correctIndex": 0
    }
  ]
};
