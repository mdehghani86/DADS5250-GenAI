#!/bin/bash
# Release the dads5250 package and re-pin every lab, in one command.
# Automates the exact flow in utils/RELEASING.md.
#
# Usage:
#   scripts/release_dads5250.sh 0.3.0            # dry run: shows what would happen
#   scripts/release_dads5250.sh 0.3.0 --publish  # the real release
#
# The real release: bumps utils/pyproject.toml, builds with uv, publishes to
# PyPI (token from ~/pypi_token.txt), tags vNEW, rewrites every lab's
# `dads5250==OLD` pin to NEW, runs the model-name linter, commits and pushes.
set -euo pipefail
cd "$(dirname "$0")/.."

NEW="${1:?usage: release_dads5250.sh <new-version> [--publish]}"
MODE="${2:-dry-run}"
OLD=$(grep -o 'version = "[0-9.]*"' utils/pyproject.toml | grep -o '[0-9.]*')

echo "current version: $OLD  ->  new version: $NEW   (mode: $MODE)"
[ "$OLD" = "$NEW" ] && { echo "ERROR: new version equals current version"; exit 1; }

PINS=$(grep -rl "dads5250==$OLD" labs --include='*.ipynb' | grep -v _archive | grep -v prompting_old | wc -l | tr -d ' ')
echo "labs currently pinned to $OLD: $PINS notebooks"

if [ "$MODE" != "--publish" ]; then
  echo "DRY RUN ONLY. Re-run with --publish to execute:"
  echo "  1. pyproject version -> $NEW"
  echo "  2. uv build utils && uv publish (token: ~/pypi_token.txt)"
  echo "  3. git tag v$NEW"
  echo "  4. re-pin $PINS notebooks to dads5250==$NEW"
  echo "  5. lint, commit, push"
  exit 0
fi

# 1. bump the version (pyproject is the source of truth; __init__ mirrors it)
sed -i '' "s/version = \"$OLD\"/version = \"$NEW\"/" utils/pyproject.toml
sed -i '' "s/__version__ = \"$OLD\"/__version__ = \"$NEW\"/" utils/dads5250/__init__.py

# 2. build fresh artifacts and publish
rm -rf utils/dist utils/build
uv build utils
uv publish --token "$(grep -o 'pypi-[A-Za-z0-9_-]*' ~/pypi_token.txt)" utils/dist/*

# 3. commit the package bump and tag
git add utils/
git commit -m "utils: dads5250 $NEW - provider registry (DeepSeek + Qwen) release"
git tag "v$NEW"

# 4. re-pin every active lab (same logic as RELEASING.md)
python3 - "$OLD" "$NEW" <<'PY'
import json, glob, sys
OLD, NEW = f"dads5250=={sys.argv[1]}", f"dads5250=={sys.argv[2]}"
count = 0
for f in glob.glob("labs/**/*.ipynb", recursive=True):
    if "_archive" in f or "prompting_old" in f:
        continue
    nb = json.load(open(f)); hit = False
    for c in nb.get("cells", []):
        src = c.get("source", [])
        # source can be a list of lines OR one long string with odd splits;
        # patch on the joined text so the pin is never missed
        joined = "".join(src) if isinstance(src, list) else src
        if OLD in joined:
            c["source"] = joined.replace(OLD, NEW).splitlines(keepends=True)
            hit = True
    if hit:
        json.dump(nb, open(f, "w"), indent=1, ensure_ascii=False)
        open(f, "a").write("\n")
        count += 1
print(f"re-pinned {count} notebooks {OLD} -> {NEW}")
PY

# 5. lint, commit, push everything
python3 scripts/check_model_names.py
git add labs/
git commit -m "labs: move to dads5250==$NEW"
git push origin main "v$NEW"

# verify it is live
sleep 20
LIVE=$(curl -s https://pypi.org/pypi/dads5250/json | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])")
echo "PyPI now serves: $LIVE (expected $NEW)"
uv run --no-project --with "dads5250==$NEW" python -c "import dads5250; print('import check ok:', dads5250.__version__ if hasattr(dads5250,'__version__') else 'ok')"
