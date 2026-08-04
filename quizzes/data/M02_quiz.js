window.QUIZ = {
  meta: { module: "M02", title: "AI in Action", subtitle: "DADS 5250 Generative AI in Practice" },
  questions: [
    {
      id: 1,
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "According to the module, what does <strong>vibe coding</strong> mean?",
      options: [
        { letter: "A", text: "Describing what you want in plain English and letting AI write the code, while you evaluate and improve it.", explanation: "Correct: vibe coding means you guide the direction in natural language and AI handles the syntax, then you verify the result." },
        { letter: "B", text: "Writing every line of code by hand while listening to music for focus.", explanation: "This confuses the casual name with the actual method. Vibe coding is not about mood or manual typing at all; it is specifically about describing the outcome you want and letting AI generate the code." },
        { letter: "C", text: "Copying finished code from documentation without any AI involvement.", explanation: "This misses that AI is central to vibe coding. The whole shift is that the model writes the code from your plain-English description, replacing the old habit of hunting through docs and memorizing syntax." },
        { letter: "D", text: "Fine-tuning a model on your own private dataset before writing any code.", explanation: "This confuses vibe coding with model training. Vibe coding uses existing models through prompts; no fine-tuning is involved, and the module frames it purely as describing outcomes and iterating." }
      ],
      correctIndex: 0
    },
    {
      id: 2,
      difficulty: "medium",
      type: "mc",
      typeLabel: "Practical insight",
      prompt: "You have a spreadsheet with thousands of rows of sales data and you want to automatically format the top products in bold and add a chart. Based on the <strong>Excel GPT</strong> lesson, what is the intended workflow?",
      options: [
        { letter: "A", text: "Describe the task in plain English to the API, get back a VBA macro, and paste it into Excel's VBA editor to run it.", explanation: "Correct: the model writes the VBA macro from your description and you paste it into Excel's VBA editor and run it." },
        { letter: "B", text: "Manually record a macro yourself first, then ask the API to explain what it does.", explanation: "This reverses the point of the tool. The lesson has the AI generate the working macro from a plain-English request, so you do not have to record or write the VBA yourself first." },
        { letter: "C", text: "Export the data to Python because Excel cannot be automated by AI-generated code.", explanation: "This assumes Excel is out of reach for AI, which the module directly contradicts. The Excel GPT tool produces both formulas and VBA macros that run inside Excel, so no export to another language is needed." },
        { letter: "D", text: "Upgrade to a special AI-only spreadsheet program, since standard Excel cannot run generated code.", explanation: "This invents a requirement that does not exist. The lab uses ordinary Excel with the same API from Module 1; you simply paste the generated formulas or macros into the standard VBA editor." }
      ],
      correctIndex: 0
    },
    {
      id: 3,
      difficulty: "medium",
      type: "mc",
      typeLabel: "Graphic based",
      prompt: "The diagram shows a pattern the module highlights across Chrome, Maps, Photoshop, Notion, and Slack. What idea is it illustrating?",
      diagram: "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg'><text x='310' y='28' text-anchor='middle' font-family='sans-serif' font-size='15' font-weight='700' fill='#1e293b'>AI as a Layer Inside Existing Tools</text><rect x='40' y='60' width='100' height='46' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='90' y='88' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#1e293b'>Chrome</text><rect x='160' y='60' width='100' height='46' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='210' y='88' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#1e293b'>Maps</text><rect x='280' y='60' width='100' height='46' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='330' y='88' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#1e293b'>Photoshop</text><rect x='400' y='60' width='80' height='46' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='440' y='88' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#1e293b'>Notion</text><rect x='500' y='60' width='80' height='46' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='540' y='88' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#1e293b'>Slack</text><line x1='90' y1='106' x2='90' y2='150' stroke='#64748b' stroke-width='1.5' marker-end='url(#a)'/><line x1='210' y1='106' x2='210' y2='150' stroke='#64748b' stroke-width='1.5' marker-end='url(#a)'/><line x1='330' y1='106' x2='330' y2='150' stroke='#64748b' stroke-width='1.5' marker-end='url(#a)'/><line x1='440' y1='106' x2='440' y2='150' stroke='#64748b' stroke-width='1.5' marker-end='url(#a)'/><line x1='540' y1='106' x2='540' y2='150' stroke='#64748b' stroke-width='1.5' marker-end='url(#a)'/><defs><marker id='a' markerWidth='8' markerHeight='8' refX='4' refY='4' orient='auto'><path d='M0,0 L8,4 L0,8 z' fill='#64748b'/></marker></defs><rect x='40' y='152' width='540' height='40' rx='6' fill='rgba(37,99,235,0.08)' stroke='#2563EB' stroke-width='2'/><text x='310' y='177' text-anchor='middle' font-family='sans-serif' font-size='13' font-weight='700' fill='#2563EB'>AI LAYER</text><text x='310' y='222' text-anchor='middle' font-family='sans-serif' font-size='12' fill='#64748b'>Same models, different interfaces</text></svg>",
      options: [
        { letter: "A", text: "AI is becoming a layer that sits inside tools you already use and quietly makes them smarter.", explanation: "Correct: the module frames AI not as a standalone product but as a horizontal layer embedded inside existing products." },
        { letter: "B", text: "Each of these companies has trained its own foundation model from scratch.", explanation: "This misreads the diagram as being about model ownership. The point is the shared AI layer and interface, and the module notes these tools are wrappers around the same underlying models, not separately trained ones." },
        { letter: "C", text: "These products must be used together in a fixed sequence to get AI features.", explanation: "This invents a dependency between the apps that the diagram does not imply. Each product independently embeds AI; the arrows show a common layer beneath them, not a required order of use." },
        { letter: "D", text: "AI only works in coding tools, so non-technical apps cannot embed it.", explanation: "This contradicts the very examples shown. Maps, Notion, and Slack are not coding tools, yet the module uses them precisely to show AI embedded across everyday, non-developer software." }
      ],
      correctIndex: 0
    },
    {
      id: 4,
      difficulty: "medium",
      type: "multi",
      typeLabel: "Multiple select",
      prompt: "Based on the module, which statements about the <strong>Bitcoin Analyzer</strong> lab are true? <em>Select all that apply.</em>",
      options: [
        { letter: "A", text: "It fetches real market price data and computes indicators such as moving averages and RSI.", explanation: "True: the lab loads real Bitcoin price data and computes returns, SMA(20/50), and RSI(14)." },
        { letter: "B", text: "It can return a structured, machine-readable JSON trade signal, not just prose.", explanation: "True: the lab asks the model for a JSON trade signal so an app can act on it, alongside the plain-English commentary." },
        { letter: "C", text: "It is presented as validated financial advice you can trade on with confidence.", explanation: "The module is explicit that this is not financial advice. It is a demonstration of AI processing real data into structured analysis, so treating its output as trading advice is a misconception." },
        { letter: "D", text: "It requires a completely different API from the one used in Module 1.", explanation: "This misses the module's core theme. The analyzer uses the same API from Module 1; only the prompt and the data change, which is exactly the point about one technology powering many applications." }
      ],
      correctIndices: [0, 1],
      explanation: "The Bitcoin Analyzer uses the same Module 1 API to fetch real data, compute indicators, and produce both prose and JSON output, but it is a demonstration of applied AI, not financial advice."
    },
    {
      id: 5,
      difficulty: "hard",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "The module says the Excel GPT and Bitcoin Analyzer sometimes gave perfect output and sometimes inconsistent output. Synthesizing this with the module's closing message, what is the <strong>gap between a demo and a product</strong>, and how does the course address it?",
      options: [
        { letter: "A", text: "The gap is reliability and consistency of output; Module 3 on prompt engineering teaches you to produce the same quality result every time.", explanation: "Correct: the gap is consistency and reliability, and the module points to prompt engineering in M03 as the way to close it." },
        { letter: "B", text: "The gap is raw model power; the fix is to switch to a larger, more expensive model in the next module.", explanation: "This assumes bigger models are the answer, but the module attributes the inconsistency to how the AI is prompted, not to model size. The stated fix is prompt engineering, using the same API, not a costlier model." },
        { letter: "C", text: "The gap is that Excel and crypto data are unusual cases; most tasks work perfectly on the first try.", explanation: "This dismisses a general lesson as a special case. The module presents inconsistent output as the normal gap between any vibe-coded prototype and a production system, not a quirk of these two domains." },
        { letter: "D", text: "The gap is that vibe coding cannot build real tools, so production requires abandoning AI-generated code.", explanation: "This contradicts the module, which shows vibe coding does build two working tools. The gap is about making that output consistent and reliable through prompt engineering, not about discarding AI-generated code." }
      ],
      correctIndex: 0
    }
  ]
};
