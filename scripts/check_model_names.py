#!/usr/bin/env python3
"""
Lint all active lab notebooks for hardcoded OpenAI / Gemini model strings in CODE cells.

Usage:
    python scripts/check_model_names.py          # exits 1 if violations found
    python scripts/check_model_names.py --fix    # rewrites notebooks in-place

Labs should always use the constants from the dads5250 utils package:
    DEFAULT_CHAT_MODEL, DEFAULT_MINI_MODEL, DEFAULT_EMBED_MODEL, DEFAULT_GEMINI_MODEL

The WHITELIST below holds patterns that are intentionally hardcoded
(e.g., fine-tune pinned model IDs, LangChain wrappers with specific aliases).
Add an entry here when a hardcode is justified — include a comment explaining why.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns that flag a hardcoded model string in a code cell source line.
# These are Python regex patterns matched against each LINE of source.
# ---------------------------------------------------------------------------
BAD_PATTERNS = [
    r'model\s*=\s*["\']gpt-',           # model="gpt-..." in any call
    r'model\s*=\s*["\']text-embedding-', # model="text-embedding-..."
    r'model\s*=\s*["\']o[134]-',         # model="o1-...", model="o3-...", model="o4-..."
    r'model\s*=\s*["\']o[134]["\']',     # model="o1", "o3", "o4" (exact)
    r'model\s*=\s*["\']gemini-',         # model="gemini-..."  (use DEFAULT_GEMINI_MODEL)
    r'model\s*=\s*["\']claude-',         # model="claude-..." (use DEFAULT_CLAUDE_MODEL)
]

# ---------------------------------------------------------------------------
# Whitelist: lines that match a bad pattern but are explicitly allowed.
# Each entry is a dict with 'file_glob' and 'pattern' (both are regexes).
# A match on BOTH means the line is whitelisted.
# ---------------------------------------------------------------------------
WHITELIST = [
    # M13 fine-tuning: OpenAI requires a pinned dated model ID for fine-tune jobs.
    {"file_glob": "M13", "pattern": r"gpt-4\.1-mini-2025-04-14"},
    # M04 LangChain: ChatGoogleGenerativeAI needs a real model alias, not gemini-flash-latest.
    {"file_glob": "M04", "pattern": r"gemini-2\.5-flash"},
]

# ---------------------------------------------------------------------------
# Replacements used by --fix mode.
# Applied IN ORDER — earlier entries take priority.
# ---------------------------------------------------------------------------
REPLACEMENTS = [
    # Fine-tune pinned model: keep as-is (whitelisted)
    # DEFAULT_MINI_MODEL covers most mini calls
    (r'model\s*=\s*"gpt-4\.1-mini"',        'model=DEFAULT_MINI_MODEL'),
    (r"model\s*=\s*'gpt-4\.1-mini'",        'model=DEFAULT_MINI_MODEL'),
    (r'model\s*=\s*"gpt-4\.1"',             'model=DEFAULT_CHAT_MODEL'),
    (r"model\s*=\s*'gpt-4\.1'",             'model=DEFAULT_CHAT_MODEL'),
    (r'model\s*=\s*"gpt-4o-mini"',          'model=DEFAULT_MINI_MODEL'),
    (r"model\s*=\s*'gpt-4o-mini'",          'model=DEFAULT_MINI_MODEL'),
    (r'model\s*=\s*"gpt-4o"',              'model=DEFAULT_CHAT_MODEL'),
    (r"model\s*=\s*'gpt-4o'",              'model=DEFAULT_CHAT_MODEL'),
    (r'model\s*=\s*"text-embedding-3-small"', 'model=DEFAULT_EMBED_MODEL'),
    (r"model\s*=\s*'text-embedding-3-small'", 'model=DEFAULT_EMBED_MODEL'),
    (r'model\s*=\s*"text-embedding-3-large"', 'model=DEFAULT_EMBED_MODEL'),
    (r"model\s*=\s*'text-embedding-3-large'", 'model=DEFAULT_EMBED_MODEL'),
]

LABS_ROOT = Path(__file__).parent.parent / "labs"
SKIP_DIRS = {"_archive", "M03_prompting_old"}


def is_whitelisted(file_path: Path, line: str) -> bool:
    for entry in WHITELIST:
        if entry["file_glob"] in str(file_path) and re.search(entry["pattern"], line):
            return True
    return False


def check_notebook(nb_path: Path, fix: bool = False) -> list[str]:
    """Return list of violation strings. If fix=True, also rewrite the file."""
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)

    violations = []
    modified = False

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        new_source = []
        for line in source:
            flagged = any(re.search(p, line) for p in BAD_PATTERNS)
            if flagged and not is_whitelisted(nb_path, line):
                if fix:
                    new_line = line
                    for pattern, replacement in REPLACEMENTS:
                        new_line = re.sub(pattern, replacement, new_line)
                    if new_line != line:
                        modified = True
                        line = new_line
                    else:
                        violations.append(f"  {nb_path.relative_to(LABS_ROOT)}  ->  {line.strip()}")
                else:
                    violations.append(f"  {nb_path.relative_to(LABS_ROOT)}  ->  {line.strip()}")
            new_source.append(line)
        cell["source"] = new_source

    if fix and modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"  fixed: {nb_path.name}")

    return violations


def main():
    fix_mode = "--fix" in sys.argv
    all_violations = []

    for nb_path in sorted(LABS_ROOT.rglob("*.ipynb")):
        # Skip archived / old dirs
        parts = set(nb_path.parts)
        if parts & SKIP_DIRS:
            continue
        violations = check_notebook(nb_path, fix=fix_mode)
        all_violations.extend(violations)

    if all_violations:
        print(f"\n{'FIXED' if fix_mode else 'VIOLATIONS'} ({len(all_violations)}):")
        for v in all_violations:
            print(v)
        if not fix_mode:
            print(
                "\nRun  python scripts/check_model_names.py --fix  to auto-fix, "
                "or replace with DEFAULT_CHAT_MODEL / DEFAULT_MINI_MODEL / DEFAULT_EMBED_MODEL."
            )
            sys.exit(1)
    else:
        print("OK  No hardcoded model strings found in code cells.")


if __name__ == "__main__":
    main()
