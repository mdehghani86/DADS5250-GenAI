# LLM provider support: decision record

Context: some students are in countries where the OpenAI / Gemini APIs are
blocked. Investigation and options: reports TEA-015 to TEA-018 in MD's
reports dashboard (2026-09-15).

| # | Decision | Challenge raised | MD's call | Success condition | Outcome |
|---|----------|------------------|-----------|-------------------|---------|
| 1 | Mechanism: provider registry inside the `dads5250` package, selected by an optional `LLM_PROVIDER` Colab Secret; `setup_openai()` keeps its name and exports `OPENAI_BASE_URL` / `OPENAI_API_BASE` / `OPENAI_API_KEY` so bare clients, LangChain and CrewAI follow automatically. | Alternatives (explicit `setup_llm()`, sibling setups, hosted proxy) ranked and presented in TEA-015/016. | Approved (registry + Secret). | A restricted student runs an unmodified lab with only 2 extra Secrets; default students see zero change. | Implemented in `utils/dads5250/api.py`; 3-mode import test passed 2026-09-15. Not yet released. |
| 2 | First provider: DeepSeek (`deepseek-v4-pro` / `deepseek-flash`). | DeepSeek has no free credits (payment barrier for some students) and no embeddings endpoint; Z.ai raised as the free alternative. | Approved DeepSeek first; Qwen next; others later. | Live `connected` check with a real `DEEPSEEK_API_KEY`. | Code in place; live test pending MD's key. |
| 3 | Ollama (local Llama) path. | Cannot run "from GitHub"; needs local install + RAM; 8B quality lower. | Dropped. | n/a | Closed 2026-09-15. |
| 4 | SDK labs (M11 x2, M12, M13_Lab3). | SDK seams (LiteLlm, chat_completions default client, Anthropic-compatible endpoints) exist but are untested and would touch 4 notebooks. | Do NOT modify the SDK labs; build ONE alternate DeepSeek-native lab covering agent/tools/handoff/guardrail concepts. | Alternate lab exists; originals stay observational for restricted students. | Planned (phase 3). |
| 5 | Embeddings gap (M01, M05, M10). | DeepSeek and Z.ai intl have no embeddings endpoint. | Qwen as second key (phase 2); local sentence-transformers fallback still open. | M05 RAG runs for a restricted student. | Implemented 2026-09-15: deepseek entry routes embeddings to Qwen (client graft + EMBED_KWARGS); M05 one-line change; full "qwen" provider added. Live test pending keys. |
| 5b | Image generation for M01_Lab2 section 3. | MD suggested Qwen; research found DashScope intl images are NOT OpenAI-shaped (native SDK + async polling) while Z.ai CogView-4 IS OpenAI-images-compatible at $0.01/image (URL-only response). | Open: MD to pick. | Restricted student generates an image from the lab. | Research done 2026-09-15; awaiting pick. |
| 6 | Pilot with a real student in an affected country before announcing. | Iran reachability claims are inference, not tested from inside. | Timing not yet decided (before vs parallel). | One student completes signup + one API call. | Open. |

Rollout gates agreed with MD: (a) live key test before release; (b) version
bump + PyPI publish + lab re-pins only on MD's explicit go (RELEASING.md flow).
