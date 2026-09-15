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
# embed_*: where /v1/embeddings calls go. OpenAI and Qwen serve embeddings on
# their own endpoint; DeepSeek has NO embeddings endpoint, so its entry routes
# embeddings to Qwen (a second, optional Colab Secret: QWEN_API_KEY).
# image_*: where /v1/images/generations calls go. Neither DeepSeek nor the
# Qwen compatible-mode endpoint serves OpenAI-shaped images, so both route to
# Z.ai's CogView (a third, optional Colab Secret: ZAI_API_KEY). CogView
# returns image URLs only (no b64_json) and expects an explicit model id.
_QWEN_BASE = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
_ZAI_BASE = "https://api.z.ai/api/paas/v4"
PROVIDERS = {
    "openai": {
        "base_url": None,                       # SDK default: api.openai.com
        "key_name": "OPENAI_API_KEY",
        "chat_model": "gpt-5.4",
        "mini_model": "gpt-5.4-mini",
        "token_param": "max_completion_tokens",
        "embed_model": "text-embedding-3-small",
        "embed_base_url": None,                 # native: same client
        "embed_key_name": None,
        "image_model": None,                    # native: the SDK's default image model
        "image_base_url": None,
        "image_key_name": None,
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "key_name": "DEEPSEEK_API_KEY",
        "chat_model": "deepseek-v4-pro",
        "mini_model": "deepseek-flash",
        "token_param": "max_tokens",
        "embed_model": "text-embedding-v4",     # served by Qwen, see below
        "embed_base_url": _QWEN_BASE,
        "embed_key_name": "QWEN_API_KEY",
        "image_model": "cogview-4-250304",      # served by Z.ai
        "image_base_url": _ZAI_BASE,
        "image_key_name": "ZAI_API_KEY",
    },
    "qwen": {
        "base_url": _QWEN_BASE,
        "key_name": "QWEN_API_KEY",
        "chat_model": "qwen3.8-max",
        "mini_model": "qwen3.8-flash",
        "token_param": "max_tokens",
        "embed_model": "text-embedding-v4",
        "embed_base_url": None,                 # native: same client
        "embed_key_name": None,
        "image_model": "cogview-4-250304",      # served by Z.ai
        "image_base_url": _ZAI_BASE,
        "image_key_name": "ZAI_API_KEY",
    },
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
DEFAULT_EMBED_MODEL = _PROVIDER["embed_model"]  # follows the embeddings backend
DEFAULT_IMAGE_MODEL = _PROVIDER["image_model"]  # None on OpenAI (SDK default); CogView id when routed
DEFAULT_GEMINI_MODEL = "gemini-flash-latest"  # auto-tracks the latest stable flash

# Kwargs for LangChain's OpenAIEmbeddings so M05-style code can follow the
# embeddings backend with one line: OpenAIEmbeddings(model=DEFAULT_EMBED_MODEL,
# **EMBED_KWARGS). Starts empty; setup_openai() fills it in place when the
# active provider routes embeddings to a second endpoint (DeepSeek -> Qwen),
# and labs imported the same dict object, so the update is visible to them.
EMBED_KWARGS = {}


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


class _BatchedEmbeddings:
    """DashScope caps embeddings batches at 10 inputs; OpenAI allows
    thousands. This thin proxy splits big batches so lab code written
    for OpenAI works unchanged on the routed backend."""
    def __init__(self, embeddings_resource, max_batch=10):
        self._emb = embeddings_resource
        self._max = max_batch

    def create(self, *, input, **kwargs):
        items = input if isinstance(input, list) else [input]
        if len(items) <= self._max:
            return self._emb.create(input=input, **kwargs)
        merged = None
        for i in range(0, len(items), self._max):
            r = self._emb.create(input=items[i:i + self._max], **kwargs)
            if merged is None:
                merged = r
            else:
                merged.data.extend(r.data)
                if getattr(merged, "usage", None) and getattr(r, "usage", None):
                    merged.usage.prompt_tokens += r.usage.prompt_tokens
                    merged.usage.total_tokens += r.usage.total_tokens
        for idx, d in enumerate(merged.data):   # re-index across the merged batches
            d.index = idx
        return merged


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
    # Embeddings routing: DeepSeek has no /v1/embeddings, so when the student
    # also set QWEN_API_KEY we graft Qwen's embeddings resource onto this
    # client. Lab cells calling client.embeddings.create(...) then just work.
    # Without the second key, chat labs run fine and we print a one-line note.
    if _PROVIDER["embed_base_url"]:
        embed_key = _get_optional(_PROVIDER["embed_key_name"])
        if embed_key:
            embed_client = OpenAI(api_key=embed_key, base_url=_PROVIDER["embed_base_url"])
            client.embeddings = _BatchedEmbeddings(embed_client.embeddings)
            # check_embedding_ctx_length=False makes LangChain send raw strings
            # (its default pre-tokenization sends token-id arrays, which
            # DashScope rejects); chunk_size=10 respects DashScope's batch cap.
            EMBED_KWARGS.update(api_key=embed_key, base_url=_PROVIDER["embed_base_url"],
                                check_embedding_ctx_length=False, chunk_size=10)
            print(f"embeddings routed to {_PROVIDER['embed_key_name'].split('_')[0].lower()}"
                  f"  |  model: {DEFAULT_EMBED_MODEL}")
        else:
            print(f"note: {LLM_PROVIDER} has no embeddings endpoint. Set "
                  f"{_PROVIDER['embed_key_name']} (Colab Secret) to enable the "
                  f"embeddings labs (M01, M05, M10).")
    # Image routing: same pattern for /v1/images/generations. Z.ai's CogView
    # is the one OpenAI-shaped image endpoint reachable for these students.
    if _PROVIDER["image_base_url"]:
        image_key = _get_optional(_PROVIDER["image_key_name"])
        if image_key:
            image_client = OpenAI(api_key=image_key, base_url=_PROVIDER["image_base_url"])
            client.images = image_client.images
            print(f"images routed to z.ai  |  model: {DEFAULT_IMAGE_MODEL}")
        else:
            print(f"note: image generation needs {_PROVIDER['image_key_name']} "
                  f"(Colab Secret); only the image section of M01 Lab 2 uses it.")
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
