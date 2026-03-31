======================================================
MODULE: M05 — Retrieval-Augmented Generation (RAG)
VIDEO: Opening — RAG
NARRATOR: Prof. Mohammad Dehghani
DURATION: 4-5 minutes (~530 words)
======================================================

PART 1: OPENING HOOK
------------------------

Imagine you are taking an open-book exam.

You have your textbook. Your notes. Your slides. Dozens of pages of reference material spread across your desk.

You do not need to memorize everything. You just need to know where to look. And how to use what you find.

That is exactly what RAG does for an AI model. It gives the model a reference library. So instead of guessing — instead of making something up because it sounds plausible — the model looks up the answer in your documents and generates a response grounded in real information.

This one idea has changed how every serious company deploys AI.

[ANIMATION: Student at desk with open books, flipping to the right page — then morphs into an AI model querying a document database and returning a highlighted answer]


PART 2: WHAT IS RAG AND WHY DO WE NEED IT?
------------------------

Here is the core problem. Large language models are trained on a snapshot of the internet. That training data has a cutoff date. It does not include your company's internal documents. It does not include last week's financial report. It does not know your product catalog.

And when the model does not know something, it does not say "I do not know." It guesses. Confidently. Convincingly. Wrong.

That is hallucination. And it is the number one reason companies hesitate to deploy AI in production.

RAG solves this in three steps.

Step one — you take your documents and split them into chunks. Paragraphs. Sections. Manageable pieces.

Step two — you convert each chunk into an embedding. A numerical fingerprint that captures the meaning of that text. You store those embeddings in a vector database.

Step three — when a user asks a question, you convert the question into an embedding, find the most similar document chunks, and pass those chunks to the model as context. The model reads them and generates an answer based on your data.

Retrieve. Then generate. That is the entire pattern.

[ANIMATION: Three-step flow — Documents split into chunks, chunks become embedding vectors stored in a database, user query finds matching vectors, matched chunks feed into the LLM alongside the question]


PART 3: REAL-WORLD EXAMPLES
------------------------

Thomson Reuters built a legal research tool using RAG. Lawyers ask questions in plain English and get answers grounded in actual case law and statutes. Not AI opinions — cited sources. It reduced research time by over 50 percent.

In engineering, Siemens uses RAG to let technicians query maintenance manuals for industrial equipment. Instead of searching through 10,000-page PDFs, they ask a question and get the exact procedure — with the page reference.

Every enterprise AI deployment I have seen in the past year uses some form of RAG. It is not optional. It is foundational.

[ANIMATION: Two panels — Lawyer querying legal database with cited sources appearing; Technician asking about a turbine repair and getting a step-by-step procedure with page numbers]


PART 4: WHY THIS MATTERS FOR YOUR CAREER
------------------------

If you want to build AI applications that companies actually trust, you need RAG. Full stop. This is the pattern that makes AI deployable in regulated industries — healthcare, finance, legal, engineering.

Knowing RAG puts you in a different category of AI engineer.


PART 5: WHAT YOU WILL BUILD
------------------------

This week, you will build a complete RAG pipeline. You will create embeddings with OpenAI. You will store them in ChromaDB — a lightweight vector database. You will write retrieval queries. And you will connect everything into a system that answers questions grounded in your own documents.

No hallucination. Just evidence-based answers.

Let us build it.

======================================================
DIGITAL MEDIA NOTES:
- The open-book exam analogy is highly relatable — consider a quick illustration or photo
- The three-step RAG flow diagram is the key visual — animate each step sequentially
- Embedding concept could use a brief visual: text turning into a grid of numbers (vector)
- Legal and engineering examples work well as side-by-side panels
- Embed a 1-question poll: "Have you ever caught an AI making something up?"
- End card: "Next: Lab — Building a RAG Pipeline with ChromaDB"
======================================================
