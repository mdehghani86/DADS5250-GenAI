import json, os
QDIR = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI/quizzes")

def Q(prompt, code, opts, correct=0):
    return {"id": 5, "difficulty": "hard", "type": "mc", "typeLabel": "Coding",
            "prompt": prompt, "code": code,
            "options": [{"letter": L, "text": t, "explanation": e} for L, (t, e) in zip("ABCD", opts)],
            "correctIndex": correct}

NEW = {
"M03": Q(
  "You give the model a tool and ask a question that needs it. At the function-calling step, what does the model return, and what does your code do next?",
  "# the model's turn returns a tool CALL, not a final answer\ntool_call = response.choices[0].message.tool_calls[0]\nname, args = tool_call.function.name, tool_call.function.arguments",
  [("The model returns a structured tool call (the function name plus JSON arguments); your code runs the function and sends the result back for the model to finish.",
    "Correct: the model requests the call, your code executes it and returns the result for the model to use."),
   ("The model runs the function itself and returns the final answer, so your code does nothing.",
    "The model cannot execute your code. It only requests a call; running the function and returning its result is your code's job."),
   ("The model returns plain prose, so you must pull the numbers out with a regex.",
    "With function calling the model returns a structured call, not free text to parse. That structure is the entire point of the feature."),
   ("The model returns the tool's source code for you to review.",
    "It returns only the call to make (name and arguments), never the function's implementation.")]),
"M04": Q(
  "In LangChain (LCEL), how do you compose a prompt, a model, and an output parser into one runnable chain?",
  "chain = prompt | llm | output_parser\nanswer = chain.invoke({\"topic\": \"supply chains\"})",
  [("Pipe them with the | operator, then call chain.invoke(...); each step's output feeds the next.",
    "Correct: LCEL composes runnables with the pipe, and invoke runs the whole sequence."),
   ("Add them together with the + operator (prompt + llm + output_parser).",
    "LCEL composes with the pipe operator |, not +. The pipe is what streams each step's output into the next."),
   ("Call each component by hand and pass results manually; LCEL has no composition operator.",
    "LCEL exists precisely so you compose components with |, instead of wiring them together by hand."),
   ("Subclass Chain and override run() for every pipeline.",
    "That is the old pre-LCEL pattern. Modern LangChain composes runnables with the pipe operator.")]),
"M05": Q(
  "In a RAG pipeline, after you embed the user's query, what does the retrieval step do in code?",
  "q_vec = embed(query)\nhits = vector_store.similarity_search(q_vec, k=4)",
  [("Compare the query vector to the stored document vectors and return the top-k most similar chunks.",
    "Correct: retrieval finds the nearest vectors in the store and returns those chunks as context."),
   ("Send the raw query text straight to the LLM and rely on it to recall the documents.",
    "That skips retrieval and brings back hallucination. RAG first fetches real chunks by vector similarity."),
   ("Concatenate every document into the prompt regardless of relevance.",
    "That wastes context and money and dilutes relevance. Retrieval selects only the top-k most similar chunks."),
   ("Re-embed all documents from scratch on every query.",
    "Document vectors are embedded once and stored; only the query is embedded per request.")]),
"M06": Q(
  "In a ReAct-style agent, what happens in code on each pass of the loop?",
  "while not done:\n    thought, action = model.decide(state)\n    observation = run_tool(action)\n    state = state + observation",
  [("The model reasons and picks a tool, your code runs it and feeds the observation back, and the loop repeats until the task is done.",
    "Correct: reason, act, observe, repeat, which is the ReAct loop."),
   ("The model returns the final answer on the first pass, so there is no loop.",
    "That is a single call, not an agent. The agent reasons and acts repeatedly until it can answer."),
   ("Every tool is called at once in parallel and the results are averaged.",
    "The agent chooses one action per step from its reasoning; it does not fire all tools and average them."),
   ("The loop always runs a fixed number of times set in advance.",
    "It continues until the agent decides the task is complete, not for a preset count.")]),
"M08": Q(
  "In CrewAI, what is the correct way to assemble and run a crew in code?",
  "crew = Crew(agents=[researcher, writer], tasks=[t1, t2], process=Process.sequential)\nresult = crew.kickoff()",
  [("Define the Agents and Tasks, pass them to Crew(agents=[...], tasks=[...], process=...), then call crew.kickoff().",
    "Correct: build the specialists and their tasks, form the crew, then kick it off."),
   ("Call each agent.run() by hand and stitch the outputs together; a Crew is unnecessary.",
    "CrewAI's value is the Crew orchestrating agents and tasks; running agents by hand throws that away."),
   ("Create the Crew first, then define the agents and tasks afterward.",
    "Agents and tasks must exist before the Crew can reference them, so they are defined first."),
   ("Call crew.train() to fine-tune a model before the crew can run.",
    "kickoff() runs the crew with existing models; there is no required training step.")]),
"M12": Q(
  "In the OpenAI Agents SDK, what is the correct way to run an agent in code?",
  "agent = Agent(name=\"Helper\", instructions=\"...\", tools=[get_weather])\nresult = await Runner.run(agent, \"What's the weather in Boston?\")\nprint(result.final_output)",
  [("Define an Agent with instructions and tools, then call Runner.run(agent, input); the Runner drives the tool and handoff loop and returns result.final_output.",
    "Correct: you describe the agent and the Runner executes the whole agentic loop."),
   ("Manually loop over tool calls and append messages yourself, exactly like the raw Chat Completions API.",
    "That is the boilerplate the SDK removes. The Runner handles the call-execute-return loop for you."),
   ("Agents run automatically as soon as they are imported, so no Runner call is needed.",
    "Nothing runs until you invoke the Runner on an agent with an input."),
   ("Call Runner.train(agent) before the agent can answer.",
    "There is no training step; Runner.run executes the agent immediately.")]),
"M13": Q(
  "In code, how does an output guardrail protect a response from leaking PII?",
  "reply = model.generate(prompt)\nif find_pii(reply):        # e.g. a regex scan of the output\n    reply = redact(reply)   # mask or block before returning",
  [("It scans the model's output (for example with a regex) and redacts or blocks it before the reply reaches the user.",
    "Correct: the guardrail inspects the generated reply and removes sensitive spans before it goes out."),
   ("It only checks the user's input and never looks at the model's output.",
    "That describes an input guardrail. An output guardrail inspects the generated reply, which is where a leak appears."),
   ("It asks the model politely not to leak PII, with no actual check in code.",
    "Relying on the prompt alone is not a guardrail. A guardrail is an independent check that runs on the output."),
   ("It encrypts the entire response so nobody can read it.",
    "Encryption is not redaction; the user still needs a readable reply. The guardrail removes only the sensitive parts.")]),
}

for mod, newq in NEW.items():
    p = os.path.join(QDIR, "data", f"{mod}_quiz.js")
    src = open(p).read()
    import re, subprocess
    # get the quiz object via node so we preserve all other questions exactly
    obj = json.loads(subprocess.check_output(["node", "-e",
        f"const vm=require('vm');const fs=require('fs');const c={{window:{{}}}};vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),c);process.stdout.write(JSON.stringify(c.window.QUIZ));",
        p]).decode())
    obj["questions"][4] = newq
    open(p, "w").write("window.QUIZ = " + json.dumps(obj, indent=2, ensure_ascii=False) + ";\n")
    print("updated coding question in", mod)
print("done")
