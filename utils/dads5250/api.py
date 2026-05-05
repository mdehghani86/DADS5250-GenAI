"""API setup and connection helpers for Colab."""

import os

# --- Default model choices (current as of 2026-05) -------------------------
# Latest OpenAI chat models that still accept a custom `temperature=` (which
# every prompting / RAG / agent lab depends on for deterministic comparisons).
# gpt-5.5 / gpt-5.3-chat-latest / gpt-5.2-chat-latest / gpt-5.1-chat-latest /
# gpt-5 / gpt-5-mini all reject custom temperature. gpt-5.4 + gpt-5.4-mini
# accept it, are the newest that do, and are the right defaults for course
# labs. To upgrade later, change these in one place.
DEFAULT_CHAT_MODEL = "gpt-5.4"          # main reasoning model
DEFAULT_MINI_MODEL = "gpt-5.4-mini"     # cheaper / faster default
DEFAULT_EMBED_MODEL = "text-embedding-3-small"
DEFAULT_GEMINI_MODEL = "gemini-flash-latest"  # auto-tracks the latest stable flash


def _get_secret(name: str) -> str:
    """Retrieve a secret from Google Colab Secrets or environment."""
    try:
        from google.colab import userdata
        return userdata.get(name)
    except (ImportError, ModuleNotFoundError):
        val = os.environ.get(name)
        if not val:
            raise EnvironmentError(
                f"'{name}' not found. In Colab: set it in Secrets (key icon). "
                f"Locally: export {name}=your-key"
            )
        return val


def setup_openai(model: str = None):
    """Set up and return an OpenAI client. Validates the key with a test call."""
    from openai import OpenAI
    model = model or DEFAULT_MINI_MODEL
    key = _get_secret("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # Quick validation — use max_completion_tokens (max_tokens is deprecated for
    # gpt-5.x family).
    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            max_completion_tokens=5,
        )
        print(f"OpenAI ready  |  model: {model}  |  status: connected")
    except Exception as e:
        print(f"OpenAI connection failed: {e}")
        raise
    return client


def setup_gemini(model: str = None):
    """Set up and return a Google GenAI client."""
    from google import genai
    model = model or DEFAULT_GEMINI_MODEL
    key = _get_secret("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    print(f"Gemini ready  |  model: {model}  |  status: connected")
    return client


def check_api(client, provider: str = "openai", model: str = None):
    """Run a quick health-check and print connection info."""
    if provider == "openai":
        model = model or DEFAULT_MINI_MODEL
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly: API is working"}],
            max_completion_tokens=10,
        )
        msg = r.choices[0].message.content.strip()
        print(f"[{provider}] {model} says: {msg}")
        return True
    elif provider == "gemini":
        model = model or DEFAULT_GEMINI_MODEL
        r = client.models.generate_content(
            model=model,
            contents="Reply with exactly: API is working",
        )
        print(f"[{provider}] {model} says: {r.text.strip()}")
        return True
    else:
        raise ValueError(f"Unknown provider: {provider}")
