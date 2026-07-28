"""
Port a refreshed AppliedGenAI lab into DADS5250.

What changes:
  - Cell 0 (markdown): replaced with the canonical DADS lab header
    (Open-in-Colab badge + DADS 5250 gradient banner with title + difficulty + time).
  - Cell 1 (code): replaced with a DADS-style setup cell that installs the
    `dads5250` package from GitHub, imports `pretty_print`, `pp`, `lab_pill`,
    and the `DEFAULT_*` model constants, calls `lab_pill(title)`, and runs
    `setup_openai()` to validate the key.

What stays byte-identical:
  - Every other code cell, every other markdown cell, in their original order.
    The educational content matches the recorded video exactly.

Usage:
    python tools/port_from_appliedgenai.py \
        --src ../AppliedGenAI/Prompting_with_API\ .ipynb \
        --dest labs/M01/M01_Lab1_API_Basics.ipynb \
        --title "M01 Lab 1 — API Basics" \
        --emoji "🚀" --difficulty Beginner --time "~15 min"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DADS_REPO = "mdehghani86/DADS5250-GenAI"
HEADER_MARKER = "dads-lab-header"
SETUP_MARKER = "dads-lab-setup"


def header_cell(dest_path: Path, title: str, emoji: str, difficulty: str, time_estimate: str) -> dict:
    rel = dest_path.as_posix()
    src = f"""<!-- {HEADER_MARKER} -->
<a href="https://colab.research.google.com/github/{DADS_REPO}/blob/main/{rel}" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

<div style="background: linear-gradient(135deg, #001a70 0%, #0055d4 100%); padding: 30px 36px; border-radius: 14px; margin-bottom: 20px;">
  <h1 style="color: #fff; margin: 0; font-size: 28px;">{emoji} {title}</h1>
  <p style="color: rgba(255,255,255,0.85); margin: 8px 0 0; font-size: 15px;">DADS 5250: Generative AI in Practice &nbsp;|&nbsp; Prof. Dehghani</p>
  <p style="color: rgba(255,255,255,0.65); margin: 6px 0 0; font-size: 13px;">⭐ Difficulty: {difficulty} &nbsp;|&nbsp; ⏱ Time: {time_estimate}</p>
</div>

> **📌 Note on models.** This lab references specific LLM versions through `DEFAULT_CHAT_MODEL` and `DEFAULT_MINI_MODEL` constants in the `dads5250` utility package. Models update quickly — feel free to swap to any newer OpenAI / Anthropic / Google model you have access to.
"""
    return {
        "cell_type": "markdown",
        "metadata": {"id": HEADER_MARKER},
        "source": src.splitlines(keepends=True),
    }


def setup_cell(title: str) -> dict:
    src = f"""# === Shared lab setup: install dads5250 + load API key + sticky pill ===
# Installs the shared utilities (pp, pretty_print, lab_pill, model constants,
# setup_openai, setup_gemini) once per Colab runtime. The same OPENAI_API_KEY
# / GEMINI_API_KEY Colab secrets are used across every DADS 5250 lab — set
# them once in the 🔑 sidebar and they're picked up automatically.
import os
import importlib.util
if importlib.util.find_spec("dads5250") is None:
    !pip install -q "git+https://github.com/{DADS_REPO}.git#subdirectory=utils"

from dads5250 import (
    pp,
    pretty_print,
    lab_pill,
    setup_openai,
    setup_gemini,
    DEFAULT_CHAT_MODEL,   # newest reasoning model that supports temperature
    DEFAULT_MINI_MODEL,   # newest mini model that supports temperature
    DEFAULT_EMBED_MODEL,  # current embeddings default
    DEFAULT_GEMINI_MODEL, # tracks the latest stable flash
)

lab_pill({title!r})            # sticky banner so you always see which lab you're in
client = setup_openai()        # loads OPENAI_API_KEY + verifies it works
"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": SETUP_MARKER},
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


def port(src_path: Path, dest_path: Path, title: str, emoji: str,
         difficulty: str, time_estimate: str) -> dict:
    nb = json.loads(src_path.read_text(encoding="utf-8"))
    cells = nb["cells"]

    # Strip any existing AppliedGenAI header / setup at indices 0..1 if they
    # match our markers; otherwise just drop the first two cells (they were
    # always the AppliedGenAI header + setup pair after the 2026-05 refresh).
    while cells and cells[0].get("metadata", {}).get("id") in {
        "applied-genai-header", "applied-genai-setup", HEADER_MARKER, SETUP_MARKER
    }:
        cells.pop(0)

    # If after stripping markers we still have a leading AppliedGenAI-style
    # header (gradient div with Applied Generative AI text), drop it too.
    if cells and cells[0]["cell_type"] == "markdown":
        first_src = "".join(cells[0]["source"])
        if "Applied Generative AI" in first_src and "linear-gradient" in first_src:
            cells.pop(0)
    if cells and cells[0]["cell_type"] == "code":
        first_src = "".join(cells[0]["source"])
        if "from utils import" in first_src and "wget" in first_src:
            cells.pop(0)

    # Prepend new DADS header + setup.
    cells.insert(0, header_cell(dest_path, title, emoji, difficulty, time_estimate))
    cells.insert(1, setup_cell(title))

    nb["cells"] = cells

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

    return {
        "src": str(src_path),
        "dest": str(dest_path),
        "title": title,
        "cells_after": len(cells),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--emoji", default="🧪")
    ap.add_argument("--difficulty", default="Intermediate",
                    choices=["Beginner", "Intermediate", "Advanced"])
    ap.add_argument("--time", default="~30 min")
    args = ap.parse_args()
    out = port(
        Path(args.src), Path(args.dest), args.title,
        args.emoji, args.difficulty, args.time,
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
