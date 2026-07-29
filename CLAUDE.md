# DADS 5250: Generative AI in Practice

## Project Overview

Graduate-level course at Northeastern University (Dept. of MIE) taught by Dr. Mohammad Dehghani.
Course teaches applied GenAI: LLM APIs, prompt engineering, LangChain, LangGraph, RAG, agents, CrewAI, MCP, workflow automation, and deployment.

## Project Structure

```
DADS5250-GenAI/
├── planning/           # Design surveys, module plan, decisions
│   ├── lab-design-survey.html   # Unified design decisions survey
│   ├── module-plan.html         # Full module plan (M01-M14)
│   ├── course-planner.html      # Old survey (reference)
│   └── design-decisions.html    # Old survey (reference)
├── labs/               # Jupyter notebooks (.ipynb) organized by module
│   ├── M01/            # Getting Started with LLM APIs
│   ├── M02/            # Prompt Engineering
│   ├── M03/            # Structured Output & Function Calling
│   ├── M04/            # LangChain & Beer Game
│   ├── M05/            # RAG
│   ├── M06/            # Agents & LangGraph
│   ├── M08/            # Multi-Agent (CrewAI)
│   ├── M09/            # Vision & Evaluation
│   ├── M10/            # GenAI Platforms
│   ├── M11/            # MCP & Guardrails
│   ├── M12/            # Workflow Automation & n8n
│   └── M13/            # Fine-Tuning & Deployment
├── utils/              # Shared Python utilities (pip-installable from GitHub)
├── course-materials/   # Lecture slides, readings
├── evaluations/        # Exams, rubrics, grading
├── data/               # Datasets for labs
├── images/             # Generated images (NanoBanana MCP)
└── .claude/commands/   # Slash commands for this project
```

## Key Decisions (from lab-design-survey.html)

- **LLM**: `gpt-4.1-mini` (primary), `gemini-2.5-flash` (free tier, 1-2 labs)
- **Repo**: By-module folders (M01/, M02/, ...)
- **Naming**: `M01_Lab1_Topic.ipynb`
- **Template**: Badge → Header → Objectives → Install → Utils → API check → Content → Exercises → Summary
- **Exercises**: 60% observational (run + analyze + submit observations), 40% code
- **Quiz**: HTML interactive, 1-3 MC questions per lab
- **Hands-on**: 2-3 per lab (fill-in / YOUR CODE HERE + embedded test functions + expected result boxes)
- **Assignment**: 1 per module
- **Lab coverage time**: 10-15 min max per lab
- **Theory/Practice**: 20/80 (lectures are separate)
- **Utils**: pip install from GitHub repo
- **Difficulty**: Star rating (1-3 stars)

## Folder Convention: assets (all modules)

Keep each module's lab folder clean. Only essential lab files live at the top of
`labs/MXX/` (the notebook or guide, the workbook, the VBA, etc.). Every
supporting or non-essential file goes under an `assets/` folder, split into
category subfolders as needed:

```
labs/MXX/
├── <essential lab files>
└── assets/
    ├── images/      # banners, diagrams, screenshots
    ├── data/        # sample datasets (if any)
    └── ...          # other categories as needed
```

Reference assets with relative links, e.g. `./assets/images/banner.png`.
When moving an existing image that a page already references, update every
reference so nothing breaks. Applies to all modules (lab folders and, where it
helps, the scripts module folders too).

## Lab Notebook Cell Convention (all labs)

Every lab notebook opens with the same two cells, in this order:

1. **Setup cell** — install the `dads5250` utils (once per runtime) and do all
   imports. No API calls here.
2. **API check cell** — call `setup_openai()` (and/or `setup_gemini()`), then a
   `pp({...}, title="API check")` that shows the connection status and the
   model(s) this lab uses. One model listed if the lab uses one, several if it
   uses several. This is a visible confirmation of connected / not connected
   before any content runs.

The key is resolved by `_get_secret()`: Colab Secret (`OPENAI_API_KEY`) first,
then an environment variable, then a hidden `getpass` prompt so a student can
enter it directly without Colab Secrets.

**Header banner image.** Cell 0 of every lab is a markdown header: the Colab
badge link, then a PNG banner image referenced by its **raw GitHub URL** (not a
relative path, which breaks in Colab). Banners live at
`labs/MXX/assets/images/<notebook>_banner.png` (navy to blue gradient, "DADS 5250
· Module N · Lab M", the lab title). The raw URL renders in both Colab and GitHub.

**Every content code cell** opens with a boxed banner header that carries the
numbered section it belongs to, e.g.

```
# ==========================================================
# 3. Compute the indicators: returns, SMA(20/50), RSI(14)
# ==========================================================
```

and important lines carry short inline comments explaining what is happening.
Numbers match the numbered markdown sections. This is required in every lab.

**Depth is required, not optional (MD has flagged thin labs repeatedly):**
- **Markdown** for each section must actually teach: motivate *why* the concept
  matters and the *need* for it, explain *how* it works in plain English, not a
  single terse sentence. The module intro must sell why the topic matters.
- **Every technical code cell** gets real inline comments — enough that a student
  can follow each non-obvious step (e.g. an `ast`/`operator` evaluator gets a
  comment per branch), not just a one-line header.
- **All model/output display uses `pretty_print(...)` or `pp(...)`**, never a bare
  `print()` of a result, and this is consistent across every cell.
- When a mechanism is introduced (tools/registration, JSON mode, embeddings,
  agents), include a short section explaining the mechanism itself before the
  first code that uses it.

## Module Plan (14 modules, 4 phases)

| Phase | Modules | Focus |
|-------|---------|-------|
| Foundations | M01-M04 | API basics, prompting, structured output, LangChain + Beer Game |
| Core | M05-M07 | RAG, Agents/LangGraph, **Hackathon** (no lab) |
| Advanced | M08-M11 | CrewAI, Vision/Eval, GenAI Platforms, MCP/Guardrails |
| Production | M12-M14 | Workflow automation (n8n), Fine-tune/Deploy, **Final Project** (no lab) |

## Slash Commands

- `/maestro` — Project manager: check progress, track modules, plan next steps
- `/gen-image` — Generate images using NanoBanana MCP (Gemini)
- `/picker` — Create visual picker HTML to compare image/style options
- `/nb-flash` — Switch NanoBanana to Flash model (faster)
- `/nb-pro` — Switch NanoBanana to Pro model (higher quality)

## GitHub

- Repo: `mdehghani86/DADS5250-GenAI` (or TwinAI-inc)
- Existing labs repo: `mdehghani86/AppliedGenAI` (18 notebooks, needs overhaul)

## Important Notes

- All labs run on Google Colab (free tier)
- API keys via Colab Secrets only (standardized names: `OPENAI_API_KEY`, `GEMINI_API_KEY`)
- LangChain 1.0+ (LCEL) — no legacy patterns
- CrewAI 0.80+ (latest decorator syntax)
- LangGraph for agentic workflows (complementary to LangChain)
- AutoGen is deprecated — mention only as reference
- Gradio/Streamlit are self-study for Hackathon prep
- React basics are self-study for Final Project
