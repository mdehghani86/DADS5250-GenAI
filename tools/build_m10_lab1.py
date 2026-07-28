"""Build DADS M10 Lab 1 — Vision & Multimodal."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from build_lab import build, md, code

LAB_PATH = Path("labs/M10/M10_Lab1_Vision_Multimodal.ipynb")
TITLE = "M10 Lab 1 — Vision & Multimodal"
EMOJI = "👁️"
DIFFICULTY = "Intermediate"
TIME = "~40 min"

body = [
    md("""<div style="background: #f0f4ff; border-left: 4px solid #0055d4; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0;">
  <h3 style="color: #001a70; margin: 0 0 8px;">🎯 Learning Objectives</h3>
  <ol style="margin: 0; color: #1a1a2e; font-size: 14px;">
    <li>Send <b>images</b> to a vision-capable LLM (URL and base64 paths)</li>
    <li>Run three core <b>vision tasks</b>: description, OCR / text extraction, structured analysis</li>
    <li>Compare <b>OpenAI vs. Gemini</b> on the same image</li>
    <li>Build a small <b>image-to-JSON</b> pipeline you could drop into a real app</li>
  </ol>
</div>
"""),

    md("""## 🧠 Why vision matters

Until this module everything you built was text in / text out. Real applications rarely live in that world — receipts, charts, screenshots, ID cards, engineering drawings, X-rays. The current generation of OpenAI, Anthropic, and Google models all *see*, and the API is barely more complicated than a chat completion: you just attach an image to the user message.

In this lab you will use the **same `client`** you have been using all course; the only new piece is the message shape.
"""),

    md("""## 1️⃣ Send an image by URL

The simplest case — the image is already hosted somewhere on the public internet. We point the model at the URL and ask a question. We use a Wikimedia Commons photo of the Eiffel Tower so this lab works with no uploads.
"""),

    code("""IMAGE_URL = "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800"  # Eiffel Tower at dusk

response = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this photo in two sentences. Focus on what is concrete (objects, time of day, weather)."},
                {"type": "image_url", "image_url": {"url": IMAGE_URL}},
            ],
        }
    ],
)

pretty_print(response.choices[0].message.content, title="🗼 Image description", theme="blue")
"""),

    md("""**What just happened?**
The `content` field of the user message used to be a plain string. For multimodal calls it becomes a *list of parts*: one or more `{"type": "text"}` parts and one or more `{"type": "image_url"}` parts. Everything else about the call is the same — temperature, system message, tools, JSON mode all still work.
"""),

    md("""## 2️⃣ Send an image by base64 (local file)

In real apps you usually do **not** have a public URL — you have a file on disk or an upload. The model accepts the same image part with a `data:` URL of base64-encoded bytes. We download the same Eiffel Tower photo into Colab and resend it that way.
"""),

    code("""import base64, urllib.request

# Pull the bytes once.
img_bytes = urllib.request.urlopen(IMAGE_URL, timeout=20).read()
img_b64 = base64.b64encode(img_bytes).decode("ascii")
print(f"image size: {len(img_bytes):,} bytes  |  base64 length: {len(img_b64):,} chars")
"""),

    code("""data_url = f"data:image/jpeg;base64,{img_b64}"

response = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What time of day was this photo taken? Justify in one sentence."},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }
    ],
)

pretty_print(response.choices[0].message.content, title="⏰ Time-of-day estimate", theme="blue")
"""),

    md("""## 3️⃣ Vision task: OCR / text extraction

A common real workload. Give the model an image with text and ask it to return *just the text*, one item per line. We use a public Wikimedia photo of a road sign.
"""),

    code("""SIGN_URL = "https://images.unsplash.com/photo-1543874768-3a4c1cccf30e?w=600"  # photo of a stop sign with text

response = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are an OCR assistant. Return only the text visible in the image, one item per line. No extra commentary.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract every legible word, number, or symbol."},
                {"type": "image_url", "image_url": {"url": SIGN_URL}},
            ],
        },
    ],
    temperature=0,
)

pretty_print(response.choices[0].message.content, title="📝 OCR output", theme="green")
"""),

    md("""## 4️⃣ Vision task: structured analysis (image → JSON)

This is the pattern you'll actually use in apps. We tell the model to return JSON with a known schema — caption, dominant colours, detected objects, a confidence score — and parse it.
"""),

    code("""import json

schema_instructions = '''Return JSON with EXACTLY these keys and no commentary:
{
  "caption": "<one sentence>",
  "dominant_colors": ["<hex>", "<hex>", "<hex>"],
  "objects": ["<object 1>", "<object 2>", ...],
  "confidence": <float 0-1>
}'''

response = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a vision tagger. " + schema_instructions},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this image."},
                {"type": "image_url", "image_url": {"url": IMAGE_URL}},
            ],
        },
    ],
    temperature=0,
)

parsed = json.loads(response.choices[0].message.content)
pp(parsed, title="🧱 Structured analysis")
"""),

    md("""## 5️⃣ Cross-provider check: same image, two models

Vision quality varies by provider. Here we run the *same* image through Gemini and compare. (You'll need a `GEMINI_API_KEY` Colab secret — same name DADS uses everywhere.)
"""),

    code("""# Run the same description prompt on Gemini.
gemini_client = setup_gemini()

gemini_response = gemini_client.models.generate_content(
    model=DEFAULT_GEMINI_MODEL,
    contents=[
        "Describe this photo in two sentences. Focus on concrete details.",
        {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
    ],
)

compare_responses({
    f"OpenAI · {DEFAULT_CHAT_MODEL}": response.choices[0].message.content,
    f"Gemini · {DEFAULT_GEMINI_MODEL}": gemini_response.text,
})
"""),

    md("""## 🎯 Hands-on exercise

1. Pick **any image URL of your own** (a chart, a meme, a photo of your screen, a hand-drawn sketch).
2. Write **one** prompt that asks the model to return JSON with at least three custom fields you actually care about — for a receipt: `merchant`, `total`, `line_items`; for a chart: `chart_type`, `x_axis`, `trend`; for a screenshot: `app_name`, `visible_buttons`.
3. Parse the JSON with `json.loads(...)` and display it with `pp(...)`.
4. **Reflect** in the cell below: where did the model get it right, and where did it hallucinate? One sentence each.

> 💡 If you're stuck on the schema, ask yourself "what would I do with this in an app?" — that question writes the schema for you.
"""),

    code("""# Your turn — replace the URL and the schema.
MY_IMAGE_URL = "https://..."

MY_SCHEMA = '''Return JSON with EXACTLY these keys: ...'''

# (write the rest)
"""),

    md("""---
*That's it for vision in. Next lab — Lab 2 — turns the lens around: we evaluate the LLM itself, systematically.*
"""),
]

if __name__ == "__main__":
    build(LAB_PATH, TITLE, EMOJI, DIFFICULTY, TIME, body)
