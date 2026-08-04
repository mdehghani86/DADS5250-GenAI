window.QUIZ = {
  meta: {
    module: "M09",
    title: "Frontend for AI: Gradio & Streamlit",
    subtitle: "DADS 5250 Generative AI in Practice"
  },
  questions: [
    {
      id: "m09-q1",
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "According to the module, what core problem do Gradio and Streamlit solve for AI builders?",
      options: [
        {
          letter: "A",
          text: "They let you turn AI code into web apps using only Python, so people who cannot run notebooks can actually use it.",
          explanation: "Correct: both are Python libraries that turn your AI code into shareable web applications, closing the gap between a notebook and a usable product."
        },
        {
          letter: "B",
          text: "They train and fine-tune the underlying language model so it produces better answers.",
          explanation: "This confuses a frontend tool with model training. Gradio and Streamlit only build the user interface around existing model calls; they do not train or fine-tune any model."
        },
        {
          letter: "C",
          text: "They replace the need to write any Python by generating the model logic automatically.",
          explanation: "This inverts how the tools work. You still write the Python function or script yourself; Gradio and Streamlit only wrap that code in a UI, they do not generate the AI logic for you."
        },
        {
          letter: "D",
          text: "They provide managed GPU servers so your model runs faster in production.",
          explanation: "This mistakes a UI library for infrastructure hosting. Neither tool provides compute or GPUs; their job is to expose your existing code as a clickable, shareable interface."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m09-q2",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Practical insight",
      prompt: "You want to text your manager a live link to a working demo of your model right now, with no deployment pipeline. Which approach does the module recommend?",
      options: [
        {
          letter: "A",
          text: "Launch the Gradio app with <code>share=True</code> to get a temporary public URL.",
          explanation: "Correct: <code>share=True</code> creates a temporary public URL (about 72 hours) with no deployment, ideal for demos and presentations."
        },
        {
          letter: "B",
          text: "Push the code to a GitHub repo and connect it to Streamlit Community Cloud.",
          explanation: "This is the deployment path for Streamlit apps, not the instant-link path. It requires a repo and a connect step, whereas the module frames <code>share=True</code> as the zero-deploy way to hand someone a link immediately."
        },
        {
          letter: "C",
          text: "Provision a Hugging Face Space and wait for the build to finish before sharing.",
          explanation: "Hugging Face Spaces gives permanent hosting, but it is a hosting step, not the instant option. The module reserves Spaces for permanent hosting and points to <code>share=True</code> when you need a link on the spot."
        },
        {
          letter: "D",
          text: "Email the <code>.ipynb</code> notebook so your manager can run the cells.",
          explanation: "This is exactly the notebook trap the module warns against. Managers and clients generally cannot run notebooks or Python, which is the whole reason a frontend link is needed."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m09-q3",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Graphic based",
      prompt: "The diagram shows the basic Gradio wiring pattern. What does the middle stage represent?",
      diagram: "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg' font-family='Outfit, sans-serif'><text x='310' y='28' text-anchor='middle' font-size='14' fill='#1e293b' font-weight='700'>Gradio Interface Pattern</text><rect x='30' y='70' width='150' height='100' rx='10' fill='rgba(37,99,235,0.08)' stroke='#2563EB' stroke-width='1.5'/><text x='105' y='108' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>inputs</text><text x='105' y='128' text-anchor='middle' font-size='10' fill='#64748b'>UI components</text><text x='105' y='144' text-anchor='middle' font-size='10' fill='#64748b'>text, image...</text><rect x='235' y='70' width='150' height='100' rx='10' fill='rgba(37,99,235,0.08)' stroke='#2563EB' stroke-width='1.5'/><text x='310' y='108' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>fn=</text><text x='310' y='128' text-anchor='middle' font-size='10' fill='#64748b'>Python</text><text x='310' y='144' text-anchor='middle' font-size='10' fill='#64748b'>function</text><rect x='440' y='70' width='150' height='100' rx='10' fill='rgba(37,99,235,0.08)' stroke='#2563EB' stroke-width='1.5'/><text x='515' y='108' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>outputs</text><text x='515' y='128' text-anchor='middle' font-size='10' fill='#64748b'>UI components</text><text x='515' y='144' text-anchor='middle' font-size='10' fill='#64748b'>return value</text><line x1='180' y1='120' x2='233' y2='120' stroke='#2563EB' stroke-width='2' marker-end='url(#a)'/><line x1='385' y1='120' x2='438' y2='120' stroke='#2563EB' stroke-width='2' marker-end='url(#a)'/><text x='310' y='205' text-anchor='middle' font-size='11' fill='#64748b'>gr.Interface(fn=..., inputs=..., outputs=...).launch()</text><defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='#2563EB'/></marker></defs></svg>",
      options: [
        {
          letter: "A",
          text: "The Python function passed as <code>fn</code>, which Gradio calls with the input values and whose return value becomes the output.",
          explanation: "Correct: Gradio wraps your <code>fn</code> so input components feed its arguments and its return value drives the output component."
        },
        {
          letter: "B",
          text: "A separate backend server you must write and deploy before the interface will run.",
          explanation: "This overcomplicates the pattern. Gradio itself starts the local server when you call <code>launch()</code>; you only supply a plain Python function, not a separate deployed backend."
        },
        {
          letter: "C",
          text: "The language model, which Gradio hosts and calls automatically.",
          explanation: "Gradio does not host or call any model on its own. The middle stage is whatever Python function you write, which may or may not call an LLM inside it."
        },
        {
          letter: "D",
          text: "A configuration file that maps input widgets to output widgets without any code.",
          explanation: "There is no widget-mapping config here. The connection between inputs and outputs is the Python function you provide as <code>fn</code>, which does the actual work."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m09-q4",
      difficulty: "medium",
      type: "multi",
      typeLabel: "Multiple select",
      prompt: "Based on the module's comparison, which statements about Streamlit are accurate? Select all that apply.",
      options: [
        {
          letter: "A",
          text: "You write a script that runs top to bottom, and each <code>st.*</code> call adds an element to the page.",
          explanation: "True: Streamlit executes the script from top to bottom on each run, and every st.* call appends an element to the page."
        },
        {
          letter: "B",
          text: "<code>st.session_state</code> remembers user inputs across reruns.",
          explanation: "True: because the script reruns on every interaction, st.session_state is what preserves values and history across those reruns."
        },
        {
          letter: "C",
          text: "<code>@st.cache_data</code> prevents expensive calls from running on every rerun.",
          explanation: "True: caching a function with @st.cache_data reuses its result, so a costly call such as a paid API does not fire on every rerun."
        },
        {
          letter: "D",
          text: "Streamlit auto-generates the interface from a single function's signature the way Gradio's <code>Interface</code> does.",
          explanation: "This is Gradio's model, not Streamlit's. Streamlit does not infer a UI from a function signature; you place each element imperatively with st.* calls as the script runs."
        }
      ],
      correctIndices: [0, 1, 2],
      explanation: "Streamlit runs a script top to bottom where each <code>st.*</code> call adds a page element, uses <code>st.session_state</code> to persist inputs across reruns, and uses <code>@st.cache_data</code> to avoid re-running expensive calls. Option D describes Gradio's function-wrapping approach; Streamlit does not infer a UI from a single function signature."
    },
    {
      id: "m09-q5",
      difficulty: "hard",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "A public Streamlit AI dashboard reruns its whole script on every widget interaction, and each rerun calls a paid LLM API and also loses the conversation so far. Which pair of fixes does the module point to?",
      options: [
        {
          letter: "A",
          text: "Wrap the expensive call with <code>@st.cache_data</code> and store the conversation in <code>st.session_state</code>.",
          explanation: "Correct: caching stops the paid call from firing on every rerun, and session state preserves inputs and history across reruns."
        },
        {
          letter: "B",
          text: "Switch the app to Gradio's <code>Interface</code>, since Gradio never reruns and has full built-in state.",
          explanation: "This misreads both tools. The module notes Gradio's state handling is limited (only session state within Blocks), and rewriting the whole app does not address the specific caching and history needs of a dashboard."
        },
        {
          letter: "C",
          text: "Move the API key into the script as a hardcoded constant so calls stop repeating.",
          explanation: "Hardcoding a key does nothing to reduce reruns or preserve history, and the module explicitly warns never to hardcode keys, recommending environment variables or secrets management instead."
        },
        {
          letter: "D",
          text: "Add <code>share=True</code> to the launch call to make the reruns cheaper.",
          explanation: "<code>share=True</code> is a Gradio setting for creating a public link, not a Streamlit feature, and sharing has nothing to do with rerun cost or preserving conversation state."
        }
      ],
      correctIndex: 0
    }
  ]
};
