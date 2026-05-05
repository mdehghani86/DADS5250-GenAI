"""
Refresh an existing DADS lab in-place: replace its first 1-3 cells (the legacy
Colab-badge + gradient-banner + learning-objectives block) with the canonical
DADS header + setup cell. Keep all educational content untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from port_from_appliedgenai import header_cell, setup_cell


def is_legacy_dads_header(src: str) -> bool:
    return any(s in src for s in [
        "colab.research.google.com/github/mdehghani86/DADS",
        "colab-badge.svg",
        "linear-gradient(135deg, #001a70",
        "Learning Objectives",
        "DADS 5250: Generative AI in Practice",
    ])


def is_legacy_setup_cell(src: str) -> bool:
    return any(s in src for s in [
        "Install Dependencies",
        "OPENAI_API_KEY",
        "from google.colab import userdata",
        "from openai import OpenAI",
        "client = OpenAI(",
    ]) and "from dads5250 import" not in src


def refresh(path: Path, title: str, emoji: str, difficulty: str, time_estimate: str) -> dict:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb["cells"]

    # Drop leading legacy header markdown blocks (up to first 3 cells).
    drops_md = 0
    while cells and cells[0]["cell_type"] == "markdown" and is_legacy_dads_header("".join(cells[0]["source"])):
        cells.pop(0)
        drops_md += 1
        if drops_md >= 3:
            break

    # Drop the first legacy setup *code* cell if it's still there.
    drops_code = 0
    if cells and cells[0]["cell_type"] == "code" and is_legacy_setup_cell("".join(cells[0]["source"])):
        cells.pop(0)
        drops_code += 1

    # Drop a "## Setup" markdown intro cell that often follows the banner.
    if cells and cells[0]["cell_type"] == "markdown":
        first = "".join(cells[0]["source"]).lstrip()
        if first.startswith("## 📦 Setup") or first.startswith("## Setup") or first.startswith("# Setup"):
            cells.pop(0)
            drops_md += 1

    # Drop another setup code cell if a "## Setup" markdown was right above it.
    if cells and cells[0]["cell_type"] == "code" and is_legacy_setup_cell("".join(cells[0]["source"])):
        cells.pop(0)
        drops_code += 1

    # Prepend canonical DADS header + setup.
    cells.insert(0, header_cell(path, title, emoji, difficulty, time_estimate))
    cells.insert(1, setup_cell(title))

    nb["cells"] = cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"path": str(path), "dropped_md": drops_md, "dropped_code": drops_code,
            "cells_after": len(cells)}


def main() -> None:
    targets = [
        ("labs/M02/M02_Lab1_Excel_GPT.ipynb",
         "M02 Lab 1 — Excel GPT", "📊", "Beginner", "~25 min"),
        ("labs/M02/M02_Lab2_Bitcoin_Analyzer.ipynb",
         "M02 Lab 2 — Bitcoin Analyzer", "📈", "Beginner", "~30 min"),
        ("labs/M03/M03_Lab2_JSON_Mode_Pydantic.ipynb",
         "M03 Lab 2 — JSON Mode & Pydantic", "🧱", "Intermediate", "~30 min"),
    ]
    for p, t, e, d, ti in targets:
        out = refresh(Path(p), t, e, d, ti)
        print(f"OK  {out['path']:60} dropped {out['dropped_md']}md+{out['dropped_code']}code  → {out['cells_after']} cells")


if __name__ == "__main__":
    main()
