======================================================
MODULE: M05 — Retrieval-Augmented Generation (RAG)
VIDEO: TA Basics — Vector Database Setup
NARRATOR: TA
DURATION: 4-5 minutes (~450 words)
======================================================

PART 1: WHAT WE ARE SETTING UP
------------------------

In this video, I will walk you through setting up ChromaDB — the vector database we will use for our RAG labs.

A vector database stores embeddings — those numerical representations of text we talked about in the opening video. Think of it as a search engine, but instead of matching keywords, it matches meaning.

ChromaDB is lightweight, runs entirely in your Colab notebook, and requires zero configuration. That is why we use it.

Let me show you how to get it running.

[ANIMATION: ChromaDB logo and tagline — "the AI-native open-source embedding database"]


PART 2: INSTALLATION
------------------------

First, install the packages. In your Colab notebook, run this cell.

pip install chromadb openai tiktoken

ChromaDB installs its own dependencies — including an embedded SQLite database. You do not need a separate server. Everything runs locally in your notebook.

If you see a warning about SQLite version, do not worry. Colab's default SQLite works fine for our use case.

One common error — if you get "chromadb not found" after installing, restart your Colab runtime. Go to Runtime, then Restart Runtime. Then re-run your import cell. This happens because Colab sometimes caches old package states.

[ANIMATION: Screen recording — Colab cell with pip install, output showing successful installation]


PART 3: CREATING YOUR FIRST COLLECTION
------------------------

Now let us create a vector database collection. A collection in ChromaDB is like a table in SQL — it holds your documents and their embeddings.

Here is the basic setup.

Import chromadb. Create a client. Create a collection with a name — something like "course-documents."

When you add documents to the collection, ChromaDB can generate embeddings for you automatically using its built-in embedding function. For our labs, we will use OpenAI's embedding model instead — text-embedding-3-small — because it gives us better quality embeddings for technical text.

You pass your documents as a list of strings. You also pass a list of unique IDs — one per document. And optionally, metadata — things like source file name, page number, or document type.

Once the documents are in, you can query by passing a question. ChromaDB converts your question into an embedding, searches for the closest matches, and returns the most relevant chunks.

[ANIMATION: Screen recording — Colab cells showing client creation, collection creation, document addition, and a sample query with results]


PART 4: COMMON ERRORS AND FIXES
------------------------

Let me save you some debugging time.

Error one — "Collection already exists." This happens if you re-run the creation cell. Use get_or_create_collection instead of create_collection. That way it grabs the existing collection if it is already there.

Error two — mismatched IDs. If you add 10 documents, you need exactly 10 IDs. No duplicates. If you see a dimension mismatch error, check your ID list.

Error three — empty results. If your query returns nothing relevant, check that your documents were actually added. Call collection.count() to verify the number of stored items.

These three cover about 90 percent of the issues students run into. If you hit something else, post it on the discussion board with your full error message.

Good luck with the lab.

======================================================
DIGITAL MEDIA NOTES:
- This should be a screen recording with voiceover — Colab notebook visible throughout
- Highlight code cells as they are discussed
- Consider callout boxes for the three common errors — red warning style
- End card: "Ready for the lab? Open M05_Lab1_RAG_Pipeline.ipynb in Colab"
======================================================
