"""Token counting and cost estimation utilities."""

import tiktoken

# Pricing per 1M tokens (input, output) — updated for current models
PRICING = {
    "gpt-4.1-mini":       (0.40, 1.60),
    "gpt-4.1":            (2.00, 8.00),
    "gpt-4.1-nano":       (0.10, 0.40),
    "gpt-4o-mini":        (0.15, 0.60),
    "gpt-4o":             (2.50, 10.00),
    "gemini-2.5-flash":   (0.15, 0.60),   # approximate
    "gemini-2.5-pro":     (1.25, 10.00),   # approximate
}


def count_tokens(text: str, model: str = "gpt-4.1-mini") -> int:
    """Count tokens in a string using tiktoken."""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4.1-mini",
) -> dict:
    """Estimate the cost of an API call.

    Returns dict with input_cost, output_cost, total_cost (in USD).
    """
    if model not in PRICING:
        return {"input_cost": None, "output_cost": None, "total_cost": None,
                "note": f"Pricing not available for {model}"}

    in_rate, out_rate = PRICING[model]
    in_cost = (input_tokens / 1_000_000) * in_rate
    out_cost = (output_tokens / 1_000_000) * out_rate

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(in_cost, 6),
        "output_cost": round(out_cost, 6),
        "total_cost": round(in_cost + out_cost, 6),
        "total_cost_str": f"${in_cost + out_cost:.6f}",
    }
