"""DADS 5250 — Shared utilities for Generative AI labs."""

from dads5250.api import (
    setup_openai, setup_gemini, check_api,
    DEFAULT_CHAT_MODEL, DEFAULT_MINI_MODEL, DEFAULT_EMBED_MODEL, DEFAULT_GEMINI_MODEL,
)
from dads5250.display import (
    pp, show_response, show_expected, show_success, show_info, compare_responses,
    pretty_print, lab_pill,
)
from dads5250.quiz import quiz
from dads5250.cost import count_tokens, estimate_cost, PRICING

__version__ = "0.2.0"
