"""
Helper for building a fresh DADS lab from scratch with the canonical header +
setup cell prepended automatically. Body cells are passed as a list of
(cell_type, source_lines) tuples.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from port_from_appliedgenai import header_cell, setup_cell


def md(source: str) -> dict:
    """Build a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    """Build a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def build(path: Path, title: str, emoji: str, difficulty: str,
          time_estimate: str, body: list[dict]) -> None:
    cells = [
        header_cell(path, title, emoji, difficulty, time_estimate),
        setup_cell(title),
        *body,
    ]
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK  {path}  ({len(cells)} cells)")
