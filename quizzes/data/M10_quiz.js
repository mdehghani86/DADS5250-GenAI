window.QUIZ = {
  meta: {
    module: "M10",
    title: "Vision, Multimodal & Evaluation",
    subtitle: "DADS 5250 Generative AI in Practice"
  },
  questions: [
    {
      id: "m10-q1",
      difficulty: "easy",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "What does it mean for a model like GPT-4o, Gemini, or Claude to be <strong>multimodal</strong>?",
      options: [
        {
          letter: "A",
          text: "It can process and reason across multiple input types such as text and images in a single interaction",
          explanation: "Correct: a multimodal model handles more than one type of input, so you can send a photo and a question together and get one integrated answer."
        },
        {
          letter: "B",
          text: "It runs on multiple GPUs at the same time to answer faster",
          explanation: "This confuses multimodal with parallel hardware. Multimodal refers to the kinds of input a model understands (text, image, audio, video), not how many processors it uses to run."
        },
        {
          letter: "C",
          text: "It can reply in several different languages",
          explanation: "Multilingual and multimodal are not the same thing. Speaking many languages is still text-only; multimodal specifically means the model accepts different modalities like images and audio, not just multiple languages."
        },
        {
          letter: "D",
          text: "It uses several separate models chained together, one per data type",
          explanation: "This describes an older pipeline of stitched unimodal models. A multimodal model processes the different input types together within the same model and conversation, which is what breaks the old unimodal boundary."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m10-q2",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Graphic based",
      prompt: "In the Lab 2 evaluation harness, each model answer is scored by three scorers before results roll up into a leaderboard. Which scorer is <strong>best suited for open-ended answers that are correct but worded very differently</strong> from the expected answer?",
      diagram: "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg' font-family='Outfit, sans-serif'><rect x='16' y='96' width='120' height='48' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='76' y='118' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>model answer</text><text x='76' y='134' text-anchor='middle' font-size='10' fill='#64748b'>+ expected</text><line x1='136' y1='120' x2='176' y2='48' stroke='#64748b' stroke-width='1.5'/><line x1='136' y1='120' x2='176' y2='120' stroke='#64748b' stroke-width='1.5'/><line x1='136' y1='120' x2='176' y2='192' stroke='#64748b' stroke-width='1.5'/><rect x='176' y='24' width='176' height='48' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='264' y='45' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>exact match</text><text x='264' y='61' text-anchor='middle' font-size='10' fill='#64748b'>string equality</text><rect x='176' y='96' width='176' height='48' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='264' y='117' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>semantic similarity</text><text x='264' y='133' text-anchor='middle' font-size='10' fill='#64748b'>embedding cosine</text><rect x='176' y='168' width='176' height='48' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='264' y='189' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>LLM-as-judge</text><text x='264' y='205' text-anchor='middle' font-size='10' fill='#64748b'>is it correct?</text><line x1='352' y1='48' x2='452' y2='108' stroke='#64748b' stroke-width='1.5'/><line x1='352' y1='120' x2='452' y2='120' stroke='#64748b' stroke-width='1.5'/><line x1='352' y1='192' x2='452' y2='132' stroke='#64748b' stroke-width='1.5'/><rect x='452' y='96' width='152' height='48' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='528' y='118' text-anchor='middle' font-size='12' fill='#1e293b' font-weight='600'>leaderboard</text><text x='528' y='134' text-anchor='middle' font-size='10' fill='#64748b'>score per model</text></svg>",
      options: [
        {
          letter: "A",
          text: "LLM-as-judge, which asks a strong model whether the answer is factually equivalent to the expected answer",
          explanation: "Correct: for open-ended answers the judge decides factual equivalence rather than matching characters, which is why the labs call it the closest scorer to human grading."
        },
        {
          letter: "B",
          text: "Exact match, because it is objective and free",
          explanation: "Exact match is objective and free but brittle. It only counts a hit when strings are identical after normalization, so a correct-but-differently-worded answer is scored wrong, which is exactly the case this question asks about."
        },
        {
          letter: "C",
          text: "Semantic similarity, because a high cosine score always means the answer is correct",
          explanation: "Semantic similarity is better than exact match at wording differences, but similarity is not the same as correctness. Two answers can look alike yet differ on the one fact that matters, so it is not the strongest choice for judging open-ended correctness."
        },
        {
          letter: "D",
          text: "None of the scorers can handle differently worded answers; you must rewrite the expected answer",
          explanation: "This misreads the harness. The whole reason the lab adds semantic similarity and especially the LLM judge is to handle answers that are right but phrased differently, so rewriting ground truth is not required."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m10-q3",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Practical insight",
      prompt: "You need to classify a batch of simple product photos with a vision API on a tight budget. Based on the module's cost guidance, what is the most sensible way to keep the API bill down?",
      options: [
        {
          letter: "A",
          text: "Resize images before sending and use low-detail mode, since it costs far fewer tokens per image for simple tasks",
          explanation: "Correct: low-detail mode runs about 85 tokens per image versus 1000+ for high detail, and resizing first avoids paying for resolution a classification task does not need."
        },
        {
          letter: "B",
          text: "Always send full-resolution images in high-detail mode so the model never misses anything",
          explanation: "High-detail mode is the most expensive option, adding 1000+ tokens per image. For simple classification it wastes money on precision you do not need; the module reserves high detail for complex images like engineering diagrams."
        },
        {
          letter: "C",
          text: "Send the images as text descriptions you write yourself so the model never sees pixels",
          explanation: "Hand-writing descriptions defeats the purpose of a vision API and would not scale to a batch. When the information is inherently visual, vision is the right tool; the savings come from resolution and detail settings, not from removing the images."
        },
        {
          letter: "D",
          text: "Vision and text calls cost the same, so no optimization is needed",
          explanation: "This is false: the module is explicit that vision calls cost more than text calls because images add tokens. Assuming parity leads to surprise bills, which is why resizing and low-detail mode are recommended."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m10-q4",
      difficulty: "medium",
      type: "mc",
      typeLabel: "Multiple choice",
      prompt: "The module argues LLM evaluation is harder than testing traditional software. What is the core reason, and what practical pattern does it recommend in response?",
      options: [
        {
          letter: "A",
          text: "LLMs are non-deterministic, so the module recommends a fixed test suite that you rerun after every change and track over time (regression testing for AI)",
          explanation: "Correct: because the same input can yield different valid outputs, you pin a fixed eval set, score every prompt or model change against it, and watch the number move."
        },
        {
          letter: "B",
          text: "LLMs are too slow to test, so the module recommends skipping evaluation until production issues appear",
          explanation: "Speed is not the issue, and skipping eval is exactly the trap the module warns against. Teams that test only manually ship silent regressions; the recommendation is to build a test suite early, not to wait for production failures."
        },
        {
          letter: "C",
          text: "LLMs are deterministic like normal code, so a single unit test with one expected output is enough",
          explanation: "This is the opposite of the module's point. LLMs are non-deterministic, so the same input can produce different outputs each run, which is precisely why one fixed input-output unit test does not work."
        },
        {
          letter: "D",
          text: "LLM outputs cannot be measured at all, so the only option is to trust that the output looks right",
          explanation: "Judging by whether output looks right is the vibes-based approach the module rejects. Outputs can be measured with metrics like exact match, semantic similarity, and an LLM judge, which turn opinion into a trackable score."
        }
      ],
      correctIndex: 0
    },
    {
      id: "m10-q5",
      difficulty: "hard",
      type: "tf",
      typeLabel: "True / False",
      prompt: "When evaluating <strong>vision</strong> model outputs, exact string matching is the recommended default because two correct image descriptions will always be worded the same way.",
      correctAnswer: false,
      explanation: "False. The module stresses that image descriptions are subjective, so two correct answers can sound completely different (for example 'a cracked bearing housing' versus 'fracture visible on the left side of the casing'), which breaks exact matching. That is why vision evaluation relies on semantic comparison, often an LLM-as-judge, rather than string matching. The common misconception is to reuse text-style exact match for vision because it is simple and objective, but it wrongly marks valid, differently phrased descriptions as failures."
    }
  ]
};
