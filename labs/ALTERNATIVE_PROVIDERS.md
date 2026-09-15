# Running the labs without OpenAI (alternative providers)

Some students are in countries where the OpenAI and Google Gemini APIs are not
available. The course labs support alternative, OpenAI-compatible providers
through the shared `dads5250` package: you add one or two extra Colab Secrets
and run the same notebooks, unchanged.

> Availability note: this switch ships with `dads5250` version 0.3.0. Labs
> pinned to an earlier version gain it automatically when the course re-pins.

## Quick start (DeepSeek)

1. Create an account at `platform.deepseek.com` (email or Google sign-in) and
   add a small credit (a few dollars covers a whole semester of labs).
2. Create an API key there.
3. In Colab, open the key sidebar (key icon) and add two Secrets, enabling
   notebook access for both:
   - `LLM_PROVIDER` with the value `deepseek`
   - `DEEPSEEK_API_KEY` with your key
4. Open any lab and Run All. The API-check cell will show
   `deepseek ready | model: deepseek-flash | status: connected`.

That is the entire setup. If `LLM_PROVIDER` is not set, everything stays on
OpenAI exactly as before, so nothing changes for anyone else.

## Embeddings labs (M01 Lab 2, M05, M10)

DeepSeek has no embeddings endpoint. For the labs that embed text, add a
third Secret:

- `QWEN_API_KEY`: from Alibaba Cloud Model Studio (international / Singapore,
  `dashscope-intl`), which gives new accounts a free token quota per model
  for 90 days, including the `text-embedding-v4` model these labs use.

With that Secret present, the package routes only the embeddings calls to
Qwen while chat stays on DeepSeek; without it, chat labs still run and the
setup cell prints a one-line note about what is missing.

## Image generation (M01 Lab 2, section 3)

The image section can also run on an alternative service, Z.ai's CogView
(about $0.01 per image). Create an account at `z.ai` (email signup), make an
API key, and add one more Secret:

- `ZAI_API_KEY`: your Z.ai key.

The package then routes image calls there automatically. Differences you
will notice: images come back as URLs (no base64 option) and are generated
at 1024x1024. Without this Secret, only that one section is unavailable.

## Jupyter / JupyterHub instead of Colab

There are no Colab Secrets there; use environment variables with the same
names before starting the notebook, for example:

```bash
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-...
export QWEN_API_KEY=sk-...    # only needed for the embeddings labs
```

or set them in the first cell with `os.environ[...] = "..."`.

## What is and is not covered

- Covered by the switch: every lab built on `chat.completions`, including
  JSON mode, function/tool calling, and vision, plus embeddings via the Qwen
  key. The provider-agnostic agents lab (`M12_Lab2_Agents_From_Scratch`)
  was written specifically to run anywhere.
- Not covered: the sections that exist to demonstrate a specific vendor's
  API (the Gemini comparisons in M04/M10, Google ADK in M11 Lab 1, Claude in
  M11 Lab 2, the OpenAI Agents SDK in M12 Lab 1 / M13 Lab 3, moderations in
  M13 Lab 2, and DALL-E image generation in M01 Lab 2). For those, follow
  the recorded run and the observational exercises; the concepts they teach
  are practiced hands-on in the provider-agnostic labs.

## Troubleshooting

- `401` or `authentication` errors: the key Secret name does not match the
  provider (`DEEPSEEK_API_KEY` for deepseek, `QWEN_API_KEY` for qwen), or
  notebook access is not enabled on the Secret.
- `model not found`: your `LLM_PROVIDER` value has a typo; the setup cell
  prints the list of valid values.
- Embeddings cells fail with a note about `QWEN_API_KEY`: add that Secret
  (see above) and re-run the setup and API-check cells.
