# Releasing the `dads5250` toolkit

The labs install the shared helpers as a versioned package: `pip install dads5250==0.2.0`.
This is the single source of truth for how to ship a change so every lab stays reproducible.

## How versions are tracked

- **Source of the code:** `utils/dads5250/` (api, display, cost, quiz).
- **Version number:** one place only, `utils/pyproject.toml` (`version = "..."`).
- **Published package:** https://pypi.org/project/dads5250/ (each version is immutable once uploaded).
- **Git tag:** every published version also gets a matching tag, e.g. `v0.2.0`.
- **Labs:** every lab setup cell pins the exact version, e.g. `!pip install -q dads5250==0.2.0`.

So a given lab always pulls the exact toolkit it was written and recorded against. Nothing
drifts. To change behavior you cut a NEW version and point the labs at it.

## Where the credentials live

- PyPI API token: `~/pypi_token.txt` (upload username is literally `__token__`).
- PyPI 2FA recovery codes: `~/pypi_recovery_codes.txt`.
- Both are owner-only files, not in any repo. Rotate the token anytime at
  pypi.org (Account settings -> API tokens); old published versions keep working.

## Cut a new version (for example 0.2.1)

Run from the repo root. `uv` is the build/publish tool (already installed).

```bash
# 1. Edit the code in utils/dads5250/ as needed.

# 2. Bump the version in utils/pyproject.toml
#    version = "0.2.1"

# 3. Build fresh artifacts
rm -rf utils/dist
uv build utils                       # produces utils/dist/dads5250-0.2.1{.tar.gz,-py3-none-any.whl}

# 4. Publish to PyPI
uv publish --token "$(grep -o 'pypi-[A-Za-z0-9_-]*' ~/pypi_token.txt)" utils/dist/*

# 5. Tag the release and push
git add utils/ && git commit -m "utils: dads5250 0.2.1 - <what changed>"
git tag v0.2.1 && git push origin main v0.2.1

# 6. Point the labs at the new version (bumps every `dads5250==0.2.0` line)
python3 - <<'PY'
import json, glob
OLD, NEW = "dads5250==0.2.0", "dads5250==0.2.1"
for f in glob.glob("labs/**/*.ipynb", recursive=True):
    if "_archive" in f or "prompting_old" in f: continue
    nb = json.load(open(f)); hit = False
    for c in nb.get("cells", []):
        s = c.get("source", [])
        for i, ln in enumerate(s):
            if OLD in ln: s[i] = ln.replace(OLD, NEW); hit = True
    if hit:
        json.dump(nb, open(f, "w"), indent=1, ensure_ascii=False)
        open(f, "a").write("\n")
PY
git add labs/ && git commit -m "labs: move to dads5250==0.2.1" && git push
```

Verify it is live and imports:

```bash
curl -s https://pypi.org/pypi/dads5250/json | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])"
uv run --no-project --with dads5250==0.2.1 python -c "import dads5250; print('ok')"
```

## Optional: auto-publish on tag

`.github/workflows/publish-pypi.yml` publishes automatically when a `v*` tag is pushed,
using PyPI Trusted Publishing (no stored token). It needs a one-time setup on pypi.org
(pending publisher) and a GitHub environment named `pypi`; steps are in the workflow header.
Until that is enabled, use the manual `uv publish` step above. Pushing the workflow file
itself needs the `workflow` OAuth scope: `gh auth refresh -h github.com -s workflow`.

## Rules of thumb

- Never re-upload the same version number; PyPI rejects it. Always bump.
- Do not edit already-recorded labs to a new version unless you re-check the video still matches.
- A lab and its recorded video are a pair; the pinned version is what keeps them in sync.
