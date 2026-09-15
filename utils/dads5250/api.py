"""API setup and connection helpers for Colab."""

import os

# --- Provider registry (restricted-country support, 2026-09) ---------------
# Some students are in countries where the OpenAI / Gemini APIs are blocked.
# Each entry here is an OpenAI-COMPATIBLE service: same `openai` python SDK,
# different base_url + key. A student switches by adding ONE extra Colab
# Secret, LLM_PROVIDER (e.g. "deepseek"), plus that provider's API key.
# Everyone else adds nothing and stays on OpenAI exactly as before.
#
# token_param: the name of the max-output-tokens argument the provider's
# models accept. gpt-5.x rejects the classic `max_tokens` and requires
# `max_completion_tokens`; DeepSeek is the reverse.
PROVIDERS = {
    "openai": {
        "base_url": None,                       # SDK default: api.openai.com
        "key_name": "OPENAI_API_KEY",
        "chat_model": "gpt-5.4",
        "mini_model": "gpt-5.4-mini",
        "token_param": "max_completion_tokens",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "key_name": "DEEPSEEK_API_KEY",
        "chat_model": "deepseek-v4-pro",
        "mini_model": "deepseek-flash",
        "token_param": "max_tokens",
    },
    # Phase 2 (planned): "qwen", the DashScope intl compatible-mode endpoint,
    # mainly for embeddings (text-embedding-v4) which DeepSeek does not offer.
}


def _get_optional(name: str):
    """Read a Colab Secret / env var WITHOUT prompting or raising.
    Used for LLM_PROVIDER, which must stay invisible to students who
    never set it (they simply get OpenAI)."""
    try:
        from google.colab import userdata
        val = userdata.get(name)
        if val:
            return val.strip()
    except Exception:
        pass
    return (os.environ.get(name) or "").strip() or None


# Provider is resolved at import time because every lab imports the model
# constants below in its setup cell, BEFORE calling setup_openai().
LLM_PROVIDER = (_get_optional("LLM_PROVIDER") or "openai").lower()
if LLM_PROVIDER not in PROVIDERS:
    print(f"Unknown LLM_PROVIDER '{LLM_PROVIDER}', falling back to 'openai'. "
          f"Valid values: {', '.join(PROVIDERS)}")
    LLM_PROVIDER = "openai"
_PROVIDER = PROVIDERS[LLM_PROVIDER]

# --- Default model choices ------------------------------------------------
# OpenAI defaults (current as of 2026-05): latest chat models that still
# accept a custom `temperature=` (which every prompting / RAG / agent lab
# depends on for deterministic comparisons). gpt-5.5 / gpt-5.3-chat-latest /
# gpt-5.2-chat-latest / gpt-5.1-chat-latest / gpt-5 / gpt-5-mini all reject
# custom temperature; gpt-5.4 + gpt-5.4-mini accept it. To upgrade later,
# change the registry above in one place.
DEFAULT_CHAT_MODEL = _PROVIDER["chat_model"]    # main reasoning model
DEFAULT_MINI_MODEL = _PROVIDER["mini_model"]    # cheaper / faster default
DEFAULT_EMBED_MODEL = "text-embedding-3-small"  # OpenAI-only for now (DeepSeek has no embeddings; Qwen planned)
DEFAULT_GEMINI_MODEL = "gemini-flash-latest"  # auto-tracks the latest stable flash


def _get_secret(name: str) -> str:
    """Retrieve a secret, trying several sources so nobody gets stuck:
    1) Google Colab Secret, 2) environment variable, 3) a hidden prompt where
    the user types/pastes the key (input is not shown or saved in the notebook).
    """
    # 1) Colab Secret
    try:
        from google.colab import userdata
        val = userdata.get(name)
        if val:
            return val
    except Exception:
        pass

    # 2) environment variable
    val = os.environ.get(name)
    if val:
        return val

    # 3) ask the user directly (hidden input)
    try:
        import getpass
        val = getpass.getpass(f"Enter your {name} (input hidden, not saved): ").strip()
    except Exception:
        val = ""
    if not val:
        raise EnvironmentError(
            f"'{name}' not found. Set it in Colab Secrets (key icon), "
            f"export {name}=your-key, or enter it when prompted."
        )
    os.environ[name] = val  # cache for the rest of this session
    return val


def setup_openai(model: str = None):
    """Set up and return an OpenAI-compatible client for the active provider
    (OpenAI by default; DeepSeek etc. when the LLM_PROVIDER secret is set).
    Validates the key with a test call."""
    from openai import OpenAI
    model = model or DEFAULT_MINI_MODEL
    key = _get_secret(_PROVIDER["key_name"])
    kwargs = {"api_key": key}
    if _PROVIDER["base_url"]:
        kwargs["base_url"] = _PROVIDER["base_url"]
        # Export the route so everything that builds its OWN client later in
        # the lab follows the same provider without any cell edits: bare
        # OpenAI() re-instantiations read OPENAI_BASE_URL, LangChain and
        # LiteLLM/CrewAI read OPENAI_API_BASE, and all of them read
        # OPENAI_API_KEY from the environment.
        os.environ["OPENAI_BASE_URL"] = _PROVIDER["base_url"]
        os.environ["OPENAI_API_BASE"] = _PROVIDER["base_url"]
        os.environ["OPENAI_API_KEY"] = key
    client = OpenAI(**kwargs)
    # Quick validation. The max-output-tokens argument is provider-specific:
    # gpt-5.x wants max_completion_tokens, DeepSeek wants max_tokens.
    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            **{_PROVIDER["token_param"]: 5},
        )
        label = "OpenAI" if LLM_PROVIDER == "openai" else LLM_PROVIDER
        print(f"{label} ready  |  model: {model}  |  status: connected")
    except Exception as e:
        print(f"{LLM_PROVIDER} connection failed: {e}")
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
            **{_PROVIDER["token_param"]: 10},
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
