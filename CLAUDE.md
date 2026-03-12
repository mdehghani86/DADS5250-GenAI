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
