"""
Split AppliedGenAI's M8_Lab1_RAG.ipynb into two DADS labs:
  - DADS M05 Lab 1: Embeddings & Vector Stores (cells 2..17)
  - DADS M05 Lab 2: RAG Pipeline (re-creates vector store, then cells 18..27)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from port_from_appliedgenai import header_cell, setup_cell


def split() -> None:
    src = Path("../AppliedGenAI/M8_Lab1_RAG.ipynb")
    nb = json.loads(src.read_text(encoding="utf-8"))
    cells = nb["cells"]

    # The original AppliedGenAI lab has the layout we mapped earlier:
    #   0 = AppliedGenAI header (drop)
    #   1 = AppliedGenAI setup (drop)
    #   2 = RAG intro image
    #   3 = pip install libraries
    #   4 = imports
    #   5..8 = explanatory markdown + duplicate api-key block (cell 7)
    #   9 = simple LangChain query (no RAG)
    #   10..12 = retrieval explanation
    #   13 = PDF document load
    #   14 = markdown
    #   15 = embedding generation + vector store
    #   16 = markdown
    #   17 = !pip install langchain-classic
    #   18 = RAG chain (retrieval + QA)
    #   19..20 = markdown
    #   21 = non-grounded LLM comparison
    #   22 = RAG with CSV
    #   23..24 = markdown
    #   25 = Hands-On HTML
    #   26 = Wikipedia exercise
    #   27 = closing markdown
    #
    # Cell 7 is the legacy "openai.api_key = userdata.get(...)" — drop it
    # since the DADS setup cell already loads the key.

    DROP_FROM_LAB1 = {0, 1, 7}
    LAB1_CELLS = [c for i, c in enumerate(cells[:18]) if i not in DROP_FROM_LAB1]

    # Lab 2 needs: install libraries + imports + doc load + embeddings + classic
    # install (so the RAG chain works), then the RAG cells 18..27.
    # We label the prerequisite cells with a callout so students know it's the
    # "rebuild what Lab 1 ended on" preamble.
    preamble_callout = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🔁 Recap from Lab 1\n",
            "\n",
            "The next four cells re-create the vector store you built at the end of Lab 1. ",
            "If you've already run Lab 1 in this session and the variables are still in scope, ",
            "you can skip them.\n",
        ],
    }
    rag_intro_callout = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🧠 The RAG Pipeline\n",
            "\n",
            "Now that you have a vector store, this lab walks through the full RAG loop: ",
            "retrieve relevant chunks → feed them as context → ground the LLM's answer.\n",
        ],
    }
    LAB2_PREREQS = [cells[3], cells[4], cells[13], cells[15], cells[17]]
    LAB2_CELLS = [preamble_callout, *LAB2_PREREQS, rag_intro_callout, *cells[18:28]]

    def write(dest: Path, body: list[dict], title: str, emoji: str,
              difficulty: str, time_estimate: str) -> None:
        new_cells = [
            header_cell(dest, title, emoji, difficulty, time_estimate),
            setup_cell(title),
            *body,
        ]
        nb_out = {**nb, "cells": new_cells}
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(nb_out, ensure_ascii=False, indent=1),
                        encoding="utf-8")
        print(f"OK  {dest}  ({len(new_cells)} cells)")

    write(Path("labs/M05/M05_Lab1_Embeddings_VectorStores.ipynb"),
          LAB1_CELLS, "M05 Lab 1 — Embeddings & Vector Stores",
          "🧬", "Intermediate", "~40 min")
    write(Path("labs/M05/M05_Lab2_RAG_Pipeline.ipynb"),
          LAB2_CELLS, "M05 Lab 2 — RAG Pipeline",
          "🔍", "Intermediate", "~45 min")


if __name__ == "__main__":
    split()
