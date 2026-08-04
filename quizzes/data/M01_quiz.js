window.QUIZ = {
  meta: { module: "M01", title: "Getting Started with LLM APIs", subtitle: "DADS 5250 Generative AI in Practice" },
  questions: [
    {
      id: 1, difficulty: "easy", type: "mc", typeLabel: "Multiple choice",
      prompt: "In an LLM API, what is a <strong>token</strong>?",
      options: [
        { letter: "A", text: "A single character of text", explanation: "Tokens are usually larger than one character. A short word is often a single token, while a long word can split into several." },
        { letter: "B", text: "A chunk of text (roughly a word or word-piece) that the model reads and generates, and that usage is billed on", explanation: "Correct. Models process text as tokens, and both context limits and cost are measured in tokens." },
        { letter: "C", text: "The secret API key used to authenticate your request", explanation: "That is an API key, a credential. It is unrelated to how text is counted." },
        { letter: "D", text: "One complete message in the conversation", explanation: "A message can contain many tokens. The token is the unit of text, not the whole message." }
      ],
      correctIndex: 1
    },
    {
      id: 2, difficulty: "medium", type: "mc", typeLabel: "Practical insight",
      prompt: "You are recording a course demo and need the model to return the <strong>exact same answer every run</strong>. Which change best achieves that?",
      options: [
        { letter: "A", text: "Raise temperature to 1.0", explanation: "Higher temperature adds randomness, so runs would differ. This is the opposite of what you want." },
        { letter: "B", text: "Set temperature to 0", explanation: "Correct. At temperature 0 the model greedily takes the most likely token each step, giving deterministic, repeatable output." },
        { letter: "C", text: "Increase max_tokens", explanation: "max_tokens only caps the length of the reply. It does not control randomness." },
        { letter: "D", text: "Turn on streaming", explanation: "Streaming only changes how the response is delivered (token by token), not what the model chooses." }
      ],
      correctIndex: 1
    },
    {
      id: 3, difficulty: "medium", type: "tf", typeLabel: "True / False",
      prompt: "True or False: increasing the <strong>temperature</strong> parameter makes the model's output more deterministic and repeatable.",
      correctAnswer: false,
      explanation: "False. Higher temperature increases randomness in token selection, so outputs vary more. Lower temperature (0) is the deterministic end."
    },
    {
      id: 4, difficulty: "medium", type: "fill", typeLabel: "Fill in",
      prompt: "To get the most <strong>deterministic, repeatable</strong> output from the API, set the temperature parameter to what numeric value?",
      accept: ["0", "0.0", "zero"],
      explanation: "Temperature 0 makes the model pick the single most likely next token at each step, so the same prompt yields the same output."
    },
    {
      id: 5, difficulty: "hard", type: "mc", typeLabel: "Multiple choice",
      prompt: "A student sends the same prompt twice at <strong>temperature 0</strong> and gets identical replies. Switching to <strong>temperature 1.2</strong>, the two replies now differ. Which statement best explains <em>both</em> observations?",
      options: [
        { letter: "A", text: "Temperature 0 caches the response, and 1.2 disables the cache", explanation: "There is no caching mechanism here. Determinism comes from how the next token is chosen, not from a cache." },
        { letter: "B", text: "At temperature 0 the model greedily selects the most likely next token, so output is fixed; higher temperature injects randomness into token selection, so outputs vary", explanation: "Correct. This single mechanism, greedy vs sampled token selection, explains both the identical and the differing runs." },
        { letter: "C", text: "Temperature only changes response speed, not the words chosen", explanation: "Temperature changes the sampling of words. If it only affected speed, the wording could not change." },
        { letter: "D", text: "The API returns random noise above temperature 1.0", explanation: "Values above 1.0 are still valid sampling settings, not noise. The text remains coherent, just more varied." }
      ],
      correctIndex: 1
    }
  ]
};
