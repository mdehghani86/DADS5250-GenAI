# Image generation for restricted students (M01_Lab2 section 3): the two options, ready to implement

Research date 2026-09-15 (sources in the reports dashboard, TEA research).
MD picks one; implementation is then a small, contained change.

## Option A: Z.ai CogView-4 (recommended: least change)

The only alternative with a true OpenAI-shaped `/images/generations` route.
$0.01 per image, email signup, no phone/card. Caveat: returns a URL only
(no `b64_json`), so the lab's b64 branch becomes a URL download.

```python
# registry addition in utils/dads5250/api.py (image fields, used by a small
# helper the lab calls; or the lab builds this client directly):
img_client = OpenAI(api_key=_get_secret("ZAI_API_KEY"),
                    base_url="https://api.z.ai/api/paas/v4")
img = img_client.images.generate(model="cogview-4-250304",
                                 prompt=prompt, size="1024x1024")
url = img.data[0].url
png_bytes = requests.get(url).content        # replaces the b64_json branch
```

Lab change: the M01_Lab2 section-3 cells gain a provider branch (or a
`get_image_client()` helper in the package chooses OpenAI vs Z.ai). One new
Colab Secret: `ZAI_API_KEY`.

Open point to verify live (2 minutes with a key): that the official openai
python SDK parses the response of the z.ai images route without complaint.

## Option B: Qwen / DashScope images (free quota, more code)

100 free images (`qwen-image-max`) on new intl accounts, but the API is the
native DashScope SDK, not OpenAI-shaped, and the wan t2i models are async
(submit + poll). Uses the same QWEN_API_KEY the embeddings path already needs.

```python
!pip install -q dashscope
import dashscope
dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
from dashscope import ImageSynthesis
rsp = ImageSynthesis.call(api_key=os.environ["QWEN_API_KEY"],
                          model="qwen-image-max",
                          prompt=prompt, n=1, size="1024*1024")
url = rsp.output.results[0].url
```

Lab change: a separate code path with a new dependency; teaches a second
SDK shape (arguably interesting, definitely more cells).

## Option C: keep the section observational

No change; restricted students watch the recorded run. Always available as
the fallback if A fails its live check.
