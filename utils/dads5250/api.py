"""API setup and connection helpers for Colab."""

import os

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


def setup_openai(model: str = "gpt-4.1-mini"):
    """Set up and return an OpenAI client. Validates the key with a test call."""
    from openai import OpenAI
    key = _get_secret("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # Quick validation
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5,
        )
        print(f"OpenAI ready  |  model: {model}  |  status: connected")
    except Exception as e:
        print(f"OpenAI connection failed: {e}")
        raise
    return client


def setup_gemini(model: str = "gemini-2.5-flash"):
    """Set up and return a Google GenAI client."""
    from google import genai
    key = _get_secret("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    print(f"Gemini ready  |  model: {model}  |  status: connected")
    return client


def check_api(client, provider: str = "openai", model: str = None):
    """Run a quick health-check and print connection info."""
    if provider == "openai":
        model = model or "gpt-4.1-mini"
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly: API is working"}],
            max_tokens=10,
        )
        msg = r.choices[0].message.content.strip()
        print(f"[{provider}] {model} says: {msg}")
        return True
    elif provider == "gemini":
        model = model or "gemini-2.5-flash"
        r = client.models.generate_content(
            model=model,
            contents="Reply with exactly: API is working",
        )
        print(f"[{provider}] {model} says: {r.text.strip()}")
        return True
    else:
        raise ValueError(f"Unknown provider: {provider}")
