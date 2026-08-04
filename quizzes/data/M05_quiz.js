window.QUIZ = {
  "meta": {
    "module": "M05",
    "title": "Retrieval-Augmented Generation (RAG)",
    "subtitle": "DADS 5250 Generative AI in Practice"
  },
  "questions": [
    {
      "id": "m05-q1",
      "difficulty": "easy",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "In this module, what core problem does RAG solve for large language models?",
      "options": [
        {
          "letter": "A",
          "text": "Hallucination -- confident but factually wrong answers about data the model never saw",
          "explanation": "Correct: RAG grounds the model in your actual documents so it retrieves real data before generating, instead of guessing."
        },
        {
          "letter": "B",
          "text": "The model is too slow, so RAG speeds up token generation",
          "explanation": "This confuses RAG with an inference optimization. RAG actually adds a retrieval step before generation, so it does not make the model generate tokens faster; its purpose is accuracy and grounding, not speed."
        },
        {
          "letter": "C",
          "text": "The model cannot understand grammar, so RAG teaches it language rules",
          "explanation": "LLMs already handle grammar fluently from pretraining. The module's point is the opposite: the model sounds fluent while inventing facts, and RAG supplies the missing factual context rather than teaching language."
        },
        {
          "letter": "D",
          "text": "The model runs out of memory, so RAG compresses its weights",
          "explanation": "This mixes RAG up with model compression or quantization. RAG does not touch the model's weights at all; it retrieves relevant document chunks and adds them to the prompt as context."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m05-q2",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Graphic based",
      "prompt": "The diagram shows a RAG pipeline at <em>query time</em>. Based on the module, what belongs in the missing <strong>Retrieve</strong> box (step 3)?",
      "diagram": "<svg viewBox='0 0 620 240' xmlns='http://www.w3.org/2000/svg' font-family='sans-serif'><defs><marker id='m05arw' markerWidth='9' markerHeight='9' refX='7' refY='3' orient='auto'><path d='M0,0 L7,3 L0,6 Z' fill='#64748b'/></marker></defs><text x='310' y='24' text-anchor='middle' font-size='13' font-weight='700' fill='#1e293b'>RAG Pipeline (Query Time)</text><rect x='16' y='70' width='104' height='60' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='68' y='96' text-anchor='middle' font-size='11' font-weight='600' fill='#1e293b'>1. Query</text><text x='68' y='112' text-anchor='middle' font-size='9' fill='#64748b'>user question</text><line x1='122' y1='100' x2='146' y2='100' stroke='#64748b' stroke-width='1.5' marker-end='url(#m05arw)'/><rect x='148' y='70' width='104' height='60' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='200' y='96' text-anchor='middle' font-size='11' font-weight='600' fill='#1e293b'>2. Embed</text><text x='200' y='112' text-anchor='middle' font-size='9' fill='#64748b'>query -&gt; vector</text><line x1='254' y1='100' x2='278' y2='100' stroke='#64748b' stroke-width='1.5' marker-end='url(#m05arw)'/><rect x='280' y='70' width='104' height='60' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB' stroke-dasharray='5 4'/><text x='332' y='96' text-anchor='middle' font-size='11' font-weight='700' fill='#2563EB'>3. Retrieve</text><text x='332' y='112' text-anchor='middle' font-size='9' fill='#64748b'>?</text><line x1='386' y1='100' x2='410' y2='100' stroke='#64748b' stroke-width='1.5' marker-end='url(#m05arw)'/><rect x='412' y='70' width='104' height='60' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='464' y='96' text-anchor='middle' font-size='11' font-weight='600' fill='#1e293b'>4. Augment</text><text x='464' y='112' text-anchor='middle' font-size='9' fill='#64748b'>add context</text><line x1='518' y1='100' x2='542' y2='100' stroke='#64748b' stroke-width='1.5' marker-end='url(#m05arw)'/><rect x='544' y='70' width='68' height='60' rx='8' fill='rgba(37,99,235,0.08)' stroke='#2563EB'/><text x='578' y='96' text-anchor='middle' font-size='11' font-weight='600' fill='#1e293b'>5. Generate</text><text x='578' y='112' text-anchor='middle' font-size='9' fill='#64748b'>answer</text><text x='310' y='176' text-anchor='middle' font-size='10' fill='#64748b'>vector store: find nearest chunk vectors</text></svg>",
      "options": [
        {
          "letter": "A",
          "text": "Search the vector store for the top-k chunks whose vectors are most similar to the query vector",
          "explanation": "Correct: retrieval embeds the query, then the vector store returns the top-k nearest chunks by meaning to use as context."
        },
        {
          "letter": "B",
          "text": "Fine-tune the LLM's weights on the query so it memorizes the answer",
          "explanation": "This treats retrieval as training. RAG never updates the model's weights at query time; the whole appeal is looking information up without any retraining, so retrieval is a similarity search over stored vectors."
        },
        {
          "letter": "C",
          "text": "Do an exact keyword string match against the raw document text",
          "explanation": "That describes keyword search, not semantic retrieval. The module contrasts the two: RAG retrieves by vector similarity so it can match meaning even when the query and chunk share no exact words."
        },
        {
          "letter": "D",
          "text": "Re-chunk and re-embed the entire document collection from scratch",
          "explanation": "Chunking and embedding the corpus happen once during indexing, not per query. At query time only the question is embedded and compared against the already-stored vectors."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": "m05-q3",
      "difficulty": "medium",
      "type": "fill",
      "typeLabel": "Fill in",
      "prompt": "In the module's RAG build, the recommended text splitter is <code>RecursiveCharacterTextSplitter</code>, and Lab 1 chunks the syllabus with a 200-character _______ between neighboring chunks so a sentence at a boundary is not cut in half. What is this shared-region setting called?",
      "accept": [
        "overlap",
        "chunk overlap",
        "chunk_overlap",
        "Overlap"
      ],
      "explanation": "The answer is overlap (chunk_overlap). A common wrong guess is 'chunk size', but chunk size sets how big each piece is; overlap is the region two neighboring chunks share so context that straddles a boundary is preserved."
    },
    {
      "id": "m05-q4",
      "difficulty": "medium",
      "type": "mc",
      "typeLabel": "Multiple choice",
      "prompt": "According to the module, what is the practical difference between chunks that are <strong>too small</strong> and chunks that are <strong>too large</strong>?",
      "options": [
        {
          "letter": "A",
          "text": "Too small loses context; too large dilutes relevance by burying the relevant text",
          "explanation": "Correct: tiny chunks can become meaningless fragments, while oversized chunks mix in so much text that the relevant part gets buried."
        },
        {
          "letter": "B",
          "text": "Too small dilutes relevance; too large loses context",
          "explanation": "This reverses the two failure modes. Small chunks lose context because a fragment may not stand on its own, and large chunks dilute relevance because the useful part is buried in surrounding text."
        },
        {
          "letter": "C",
          "text": "Chunk size has no effect on retrieval quality; only the embedding model matters",
          "explanation": "The module treats chunking as one of the most important RAG decisions. Both size and overlap directly shape what the model retrieves, so chunk size very much affects retrieval quality."
        },
        {
          "letter": "D",
          "text": "Smaller chunks are always better because they cost less to embed",
          "explanation": "Cost is not the deciding factor, and smaller is not always better. Chunks that are too small strip away the context needed to answer, which is why the module recommends a balanced size of roughly 500-1000 characters."
        }
      ],
      "correctIndex": 0
    },
    {
      "id": 5,
      "difficulty": "hard",
      "type": "mc",
      "typeLabel": "Coding",
      "prompt": "In a RAG pipeline, after you embed the user's query, what does the retrieval step do in code?",
      "code": "q_vec = embed(query)\nhits = vector_store.similarity_search(q_vec, k=4)",
      "options": [
        {
          "letter": "A",
          "text": "Compare the query vector to the stored document vectors and return the top-k most similar chunks.",
          "explanation": "Correct: retrieval finds the nearest vectors in the store and returns those chunks as context."
        },
        {
          "letter": "B",
          "text": "Send the raw query text straight to the LLM and rely on it to recall the documents.",
          "explanation": "That skips retrieval and brings back hallucination. RAG first fetches real chunks by vector similarity."
        },
        {
          "letter": "C",
          "text": "Concatenate every document into the prompt regardless of relevance.",
          "explanation": "That wastes context and money and dilutes relevance. Retrieval selects only the top-k most similar chunks."
        },
        {
          "letter": "D",
          "text": "Re-embed all documents from scratch on every query.",
          "explanation": "Document vectors are embedded once and stored; only the query is embedded per request."
        }
      ],
      "correctIndex": 0
    }
  ]
};
