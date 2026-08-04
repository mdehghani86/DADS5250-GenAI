window.QUIZ = {
  "meta": {
    "module": "M03",
    "title": "Prompt Engineering, Structured Output & Function Calling",
    "subtitle": "DADS 5250 Generative AI in Practice"
  },
  "questions": [
    {
      "id": "m03q1",
      "difficulty": "easy",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "In the RTCF framework taught in this module, what do the four letters stand for?",
      "options": [
        {
          "letter": "A",
          "text": "Role, Task, Context, Format",
          "explanation": "Correct: RTCF stands for Role, Task, Context, and Format, the four elements every good prompt should have."
        },
        {
          "letter": "B",
          "text": "Reason, Test, Compute, Finish",
          "explanation": "This invents a reasoning loop that is not the RTCF framework. RTCF is a prompt-writing checklist standing for Role, Task, Context, Format, not steps in an execution process."
        },
        {
          "letter": "C",
          "text": "Request, Token, Cost, Fallback",
          "explanation": "This mixes API and billing terms that are unrelated to the prompt framework. RTCF describes prompt content and stands for Role, Task, Context, Format."
        },
        {
          "letter": "D",
          "text": "Retrieval, Training, Chaining, Fine-tuning",
          "explanation": "These are advanced pipeline techniques from later modules, not the prompt anatomy. RTCF is the four-part structure of a single prompt: Role, Task, Context, Format."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m03q2",
      "difficulty": "medium",
      "type": "multi",
      "typeLabel": "Multiple select",
      "prompt": "The module presents three core prompting <strong>strategies</strong>. Which of the following are among them as taught?",
      "options": [
        {
          "letter": "A",
          "text": "Zero-shot: give the task with no examples",
          "explanation": "Correct: zero-shot gives the model a task with no examples and works for simple, familiar tasks."
        },
        {
          "letter": "B",
          "text": "Few-shot: give a few examples before the task",
          "explanation": "Correct: few-shot supplies a few examples so the model learns the pattern, useful for consistent formatting and edge cases."
        },
        {
          "letter": "C",
          "text": "Chain-of-thought: tell the model to think step by step",
          "explanation": "Correct: chain-of-thought asks the model to reason step by step and improves accuracy on multi-step reasoning problems like the bat-and-ball puzzle."
        },
        {
          "letter": "D",
          "text": "Fine-tuning: retrain the model weights on your examples",
          "explanation": "This confuses a prompting strategy with model training. Fine-tuning changes the model's weights and is covered in a later production module; the three prompting strategies here are zero-shot, few-shot, and chain-of-thought, none of which retrain the model."
        }
      ],
      "correctIndices": [
        0,
        1,
        2
      ],
      "explanation": "The three prompting strategies taught are zero-shot, few-shot, and chain-of-thought. Fine-tuning is not a prompting strategy, it retrains the model and belongs to a later module."
    },
    {
      "id": "m03q3",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Graphic based",
      "prompt": "The diagram shows the function-calling loop from Section 3. At the highlighted step where the model responds to <em>\"What is the weather in Boston?\"</em>, what does the model actually return?",
      "diagram": "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg'><text x='310' y='24' text-anchor='middle' font-family='sans-serif' font-size='14' fill='#1e293b' font-weight='700'>Function-Calling Loop</text><rect x='20' y='60' width='150' height='60' rx='8' fill='#eff6ff' stroke='#2563EB' stroke-width='2'/><text x='95' y='86' text-anchor='middle' font-family='sans-serif' font-size='11' fill='#1e293b' font-weight='600'>1. You send</text><text x='95' y='102' text-anchor='middle' font-family='sans-serif' font-size='10' fill='#64748b'>question + tools</text><rect x='235' y='60' width='150' height='60' rx='8' fill='#2563EB' stroke='#1e293b' stroke-width='2'/><text x='310' y='84' text-anchor='middle' font-family='sans-serif' font-size='11' fill='#ffffff' font-weight='700'>2. Model returns</text><text x='310' y='100' text-anchor='middle' font-family='sans-serif' font-size='10' fill='#dbeafe'>a tool call (JSON)</text><rect x='450' y='60' width='150' height='60' rx='8' fill='#eff6ff' stroke='#2563EB' stroke-width='2'/><text x='525' y='86' text-anchor='middle' font-family='sans-serif' font-size='11' fill='#1e293b' font-weight='600'>3. You execute</text><text x='525' y='102' text-anchor='middle' font-family='sans-serif' font-size='10' fill='#64748b'>the real function</text><rect x='235' y='160' width='150' height='60' rx='8' fill='#eff6ff' stroke='#2563EB' stroke-width='2'/><text x='310' y='186' text-anchor='middle' font-family='sans-serif' font-size='11' fill='#1e293b' font-weight='600'>4. You return result</text><text x='310' y='202' text-anchor='middle' font-family='sans-serif' font-size='10' fill='#64748b'>model answers</text><path d='M170 90 L232 90' stroke='#64748b' stroke-width='2' marker-end='url(#a)'/><path d='M385 90 L447 90' stroke='#64748b' stroke-width='2' marker-end='url(#a)'/><path d='M525 120 L525 145 L387 145' stroke='#64748b' stroke-width='2' marker-end='url(#a)'/><path d='M235 175 L110 175 L110 122' stroke='#64748b' stroke-width='2' stroke-dasharray='4,3' marker-end='url(#a)'/><defs><marker id='a' markerWidth='8' markerHeight='8' refX='6' refY='3' orient='auto'><path d='M0,0 L6,3 L0,6 Z' fill='#64748b'/></marker></defs></svg>",
      "options": [
        {
          "letter": "A",
          "text": "A structured tool call naming the function and its arguments, such as get_weather with city \"Boston\"",
          "explanation": "Correct: instead of prose, the model returns a structured call naming the function and the arguments it pulled from the sentence."
        },
        {
          "letter": "B",
          "text": "A finished sentence like \"It is 72 degrees in Boston\"",
          "explanation": "This assumes the model answers directly, but at step 2 it has no live weather data. The human-readable sentence only comes in step 4 after your code executes the function and returns the result."
        },
        {
          "letter": "C",
          "text": "The model runs the weather function itself and returns the value",
          "explanation": "This is the common misconception that the model executes tools. The model never runs your code; it only emits a structured request, and your code performs the execution in step 3."
        },
        {
          "letter": "D",
          "text": "A Pydantic model instance validating the weather schema",
          "explanation": "This confuses structured output from Section 2 with function calling. The model returns a JSON tool call, not a Pydantic object; Pydantic is a separate validation layer you apply in your own code."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m03q4",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "The module says JSON mode has a gap that Pydantic fills. What is that gap?",
      "options": [
        {
          "letter": "A",
          "text": "JSON mode guarantees valid JSON but not the right fields or the right types; Pydantic validates the schema",
          "explanation": "Correct: JSON mode guarantees parseable JSON, but only Pydantic enforces that the expected fields exist with the correct types."
        },
        {
          "letter": "B",
          "text": "JSON mode cannot return numbers, so Pydantic converts strings to numbers",
          "explanation": "This misstates JSON mode, which can return numbers, booleans, and lists. The real gap is that JSON mode does not guarantee the correct fields or types, which is what Pydantic checks."
        },
        {
          "letter": "C",
          "text": "JSON mode often returns malformed JSON wrapped in markdown, and Pydantic strips the markdown",
          "explanation": "That describes asking for JSON without JSON mode; JSON mode itself guarantees valid, parseable JSON. Pydantic's job is validating fields and types, not cleaning markdown."
        },
        {
          "letter": "D",
          "text": "JSON mode is slower, so Pydantic caches the responses for speed",
          "explanation": "Pydantic is a validation library, not a cache, and speed is not the issue. The gap is correctness: JSON mode ensures valid JSON but not the right schema, which Pydantic enforces."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": 5,
      "difficulty": "hard",
      "type": "mc",
      "typeLabel": "Coding",
      "prompt": "You give the model a tool and ask a question that needs it. At the function-calling step, what does the model return, and what does your code do next?",
      "code": "# the model's turn returns a tool CALL, not a final answer\ntool_call = response.choices[0].message.tool_calls[0]\nname, args = tool_call.function.name, tool_call.function.arguments",
      "options": [
        {
          "letter": "A",
          "text": "The model returns a structured tool call (the function name plus JSON arguments); your code runs the function and sends the result back for the model to finish.",
          "explanation": "Correct: the model requests the call, your code executes it and returns the result for the model to use."
        },
        {
          "letter": "B",
          "text": "The model runs the function itself and returns the final answer, so your code does nothing.",
          "explanation": "The model cannot execute your code. It only requests a call; running the function and returning its result is your code's job."
        },
        {
          "letter": "C",
          "text": "The model returns plain prose, so you must pull the numbers out with a regex.",
          "explanation": "With function calling the model returns a structured call, not free text to parse. That structure is the entire point of the feature."
        },
        {
          "letter": "D",
          "text": "The model returns the tool's source code for you to review.",
          "explanation": "It returns only the call to make (name and arguments), never the function's implementation."
        }
      ],
      "correctIndex": 0
    }
  ]
};
