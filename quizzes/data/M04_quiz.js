window.QUIZ = {
  meta: { module: "M04", title: "LangChain & the Beer Game", subtitle: "DADS 5250 Generative AI in Practice" },
  questions: [
    {
      id: 1,
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "According to Module 4, what are the <strong>four core building blocks</strong> of LangChain?",
      options: [
        { letter: "A", text: "LLMs, Prompt Templates, Memory, and Chains", explanation: "Correct: the module names LLMs, Prompt Templates, Memory, and Chains as the four building blocks that LCEL connects together." },
        { letter: "B", text: "Embeddings, Vector Stores, Retrievers, and Rerankers", explanation: "These are components of a RAG pipeline, not the four LangChain building blocks. RAG and retrieval are covered in the next module, whereas Module 4 focuses on LLMs, Prompt Templates, Memory, and Chains." },
        { letter: "C", text: "Agents, Tools, Planners, and Executors", explanation: "These terms belong to agentic frameworks like LangGraph, not the foundational blocks taught here. Module 4's four blocks are LLMs, Prompt Templates, Memory, and Chains." },
        { letter: "D", text: "Tokens, Weights, Layers, and Gradients", explanation: "These describe the internals of a neural network, not LangChain's application-level components. LangChain composes LLMs, Prompt Templates, Memory, and Chains rather than exposing model internals." }
      ],
      correctIndex: 0
    },
    {
      id: 2,
      difficulty: "medium",
      type: "order",
      typeLabel: "Ordering",
      prompt: "Order the stages of a basic LCEL chain so that data flows correctly from a user's question to a clean answer, as shown in <em>Building Your First Chain</em>.",
      items: [
        "The LLM generates a raw response",
        "The user asks a question",
        "The output parser extracts the clean text",
        "The prompt template wraps the input with structure and context"
      ],
      correctOrder: [2, 0, 3, 1],
      explanation: "The correct sequence is: the user asks a question, the prompt template wraps it with structure and context, the LLM generates a raw response, then the output parser extracts the clean text. This mirrors the LCEL pipeline prompt | llm | output_parser, where each step's output becomes the next step's input."
    },
    {
      id: 3,
      difficulty: "medium",
      type: "mc",
      typeLabel: "Practical insight",
      prompt: "In LangChain's unified interface, you swap from <code>ChatOpenAI</code> to <code>ChatGoogleGenerativeAI</code>. What is the main practical benefit the module highlights?",
      options: [
        { letter: "A", text: "You change providers in essentially one line without rewriting the rest of the application", explanation: "Correct: the unified interface means the same code sends identical messages to different providers, so you swap models in one line without rewriting the pipeline." },
        { letter: "B", text: "The two models will now always return identical answers", explanation: "Different providers produce different outputs even with the same input, so identical answers are not guaranteed. The benefit is code portability, not response equivalence: the same code runs on either model, but each still reasons and phrases things differently." },
        { letter: "C", text: "Memory is automatically shared across both providers with no extra setup", explanation: "Swapping the LLM does not by itself wire up memory; LLMs are stateless by default and memory is a separate building block you add. The unified interface only standardizes how you call any model, not conversation state." },
        { letter: "D", text: "It removes the need for prompt templates entirely", explanation: "Prompt templates and the model interface are independent building blocks, so changing the model does not eliminate templates. Templates still provide reusable, variable-filled prompts regardless of which provider you call." }
      ],
      correctIndex: 0
    },
    {
      id: 4,
      difficulty: "medium",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "In the Beer Game, what is the <strong>bullwhip effect</strong> that emerges over the simulation?",
      options: [
        { letter: "A", text: "Small changes in customer demand amplify into progressively larger order swings upstream toward the factory", explanation: "Correct: because each role reacts to the order below it (with delays), small demand changes grow into massive swings as you move up toward the factory." },
        { letter: "B", text: "Orders shrink steadily at each stage until the factory produces almost nothing", explanation: "The bullwhip effect amplifies rather than dampens variation, so orders swing wider upstream, not smaller. Demand distortion grows toward the factory, which is the opposite of a steady shrink." },
        { letter: "C", text: "The retailer and factory always place exactly the same order every week", explanation: "Identical, stable orders would mean no bullwhip at all, yet the whole point of the simulation is that upstream orders become more volatile. Delays and overreaction make the factory's orders swing far more than the retailer's." },
        { letter: "D", text: "Holding cost is eliminated once the AI agents coordinate their orders", explanation: "The bullwhip effect describes demand amplification, not the removal of holding cost, and the simulation still tracks holding and backorder costs throughout. Coordination might reduce swings, but the effect itself is about amplified variability, not cost elimination." }
      ],
      correctIndex: 0
    },
    {
      id: 5,
      difficulty: "hard",
      type: "mc",
      typeLabel: "Coding",
      prompt: "A simplified Beer Game loop passes each role's order to the next role upstream, adding a fixed buffer at every stage (a stand-in for overreaction). What does this snippet print?",
      code: "roles = [\"Retailer\", \"Wholesaler\", \"Distributor\", \"Factory\"]\norder = 4\nfor role in roles:\n    order = order + 2\n    print(role, order)",
      options: [
        { letter: "A", text: "Retailer 6 / Wholesaler 8 / Distributor 10 / Factory 12", explanation: "Correct: order starts at 4 and gains 2 before each print, producing Retailer 6, Wholesaler 8, Distributor 10, Factory 12 (one line each)." },
        { letter: "B", text: "Retailer 4 / Wholesaler 6 / Distributor 8 / Factory 10", explanation: "This assumes the print happens before the addition, but order = order + 2 runs first each iteration. The Retailer therefore prints 6, not 4, and every line is 2 higher than shown." },
        { letter: "C", text: "Retailer 6 / Wholesaler 6 / Distributor 6 / Factory 6", explanation: "This treats order as if it reset to 4 each loop, but order is defined once outside the loop and carries its value forward. Because it accumulates, the amount grows by 2 at every stage instead of staying constant." },
        { letter: "D", text: "Factory 12 / Distributor 10 / Wholesaler 8 / Retailer 6", explanation: "The list is iterated in its written order, Retailer first, so the output is not reversed. The values are right but the roles print top to bottom starting with Retailer." }
      ],
      correctIndex: 0
    }
  ]
};
