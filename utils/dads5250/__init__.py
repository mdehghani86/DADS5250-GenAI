"""DADS 5250 — Shared utilities for Generative AI labs."""

from dads5250.api import setup_openai, setup_gemini, check_api
from dads5250.display import show_response, show_expected, show_success, show_info, compare_responses
from dads5250.quiz import quiz
from dads5250.cost import count_tokens, estimate_cost, PRICING

__version__ = "0.1.0"
