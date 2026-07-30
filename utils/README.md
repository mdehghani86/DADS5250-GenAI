# dads5250

Shared utilities for **DADS 5250: Generative AI in Practice** (Northeastern University, MIE).
Small, dependency light helpers that every course lab imports so the notebooks stay short and
consistent: API setup, pretty output boxes, token and cost helpers, and inline quizzes.

## Install

Once published to PyPI:

```bash
pip install dads5250
```

Pinned install straight from the course repo (works today, reproducible):

```bash
pip install "git+https://github.com/mdehghani86/DADS5250-GenAI.git@v0.2.0#subdirectory=utils"
```

Optional Gemini support:

```bash
pip install "dads5250[gemini]"
```

## What is inside

| Module | Purpose |
|--------|---------|
| `api` | `setup_openai`, `setup_gemini`, `check_api`, default model names, key resolution (Colab Secret then env then hidden prompt) |
| `display` | `pp`, `pretty_print`, `show_response`, `compare_responses`, `lab_pill` and other styled output boxes |
| `cost` | token counting and cost estimate helpers |
| `quiz` | lightweight inline multiple choice quizzes for labs |

## Usage

```python
from dads5250 import setup_openai, pp, DEFAULT_MINI_MODEL

client = setup_openai()
resp = client.chat.completions.create(
    model=DEFAULT_MINI_MODEL,
    messages=[{"role": "user", "content": "Say hello"}],
)
pp(resp.choices[0].message.content, title="Model reply")
```

## Versioning

Labs pin a released tag (for example `@v0.2.0`) so a notebook downloaded from Canvas keeps
working even if the repository changes later. Bump the version in `pyproject.toml`, tag the
commit, and the labs move to the new version only when their install line is updated.
