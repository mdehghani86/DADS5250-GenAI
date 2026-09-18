# Recording brief: API key setup videos (2 videos)

For: TA Saqar Esmaeili
Status: DRAFT. Do not record yet. MD must confirm the two video split below first.
Companion page: `course-materials/canvas/API_Key_Setup_Jupyter.html` (the videos
demonstrate exactly what that page says; do not improvise extra advice).

## Proposed split, for MD to confirm

- Video 1: "Set your key in Jupyter" (the happy path, target 3:00)
- Video 2: "When the key does not work" (the four failures, target 3:30)

Why this split and not Colab vs Jupyter: the page is scoped to students outside
vLab using their own Jupyter, so both videos live there. Splitting happy path
from troubleshooting matches how students actually watch: everyone watches
video 1 once; video 2 is opened only by a student who is stuck, and that
student wants to jump straight to their error, not scrub past setup they
already did. It also keeps both videos under four minutes.

## Rules for both videos

- NEVER show a real key. All demos run on DeepSeek. Before recording, create
  a throwaway key on the DeepSeek dashboard, and REVOKE it immediately after recording. Even better:
  where the key would be typed, the hidden getpass prompt shows nothing anyway,
  which is part of the lesson.
- Do not open the provider dashboard on camera while logged in to a personal
  account. If the dashboard must appear, log in before recording, pause on the
  API keys page, and crop or blur anything personal (name, email, billing).
- Clean screen: fresh browser profile or guest window, no bookmarks bar, no
  email tab, notifications off, desktop hidden.
- Zoom Jupyter to at least 125 percent so code is readable at 1080p.
- Microphone only, no webcam needed. Plain screen recording.
- Record on the host the course actually embeds from. Check with MD whether
  this goes to Panopto or Canvas Studio before uploading; the embed shapes
  differ and a wrong host id gives an empty player.

## Video 1: Set your key in Jupyter (target 3:00)

| # | On screen | Say roughly | Time |
|---|---|---|---|
| 1 | Empty Jupyter notebook, one markdown cell titled "DADS 5250 lab" | "If you run the labs on your own computer instead of vLab or Colab, you set your API key once per session. It takes under a minute." | 0:15 |
| 2 | Type the Step 2 cell exactly as on the Canvas page: `import os, getpass`, then `os.environ["LLM_PROVIDER"] = "deepseek"`, then `os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Paste your DeepSeek API key: ").strip()` | "The first line points the course toolkit at DeepSeek. The second asks for the key with a hidden prompt: the key never appears on screen and never lands inside the notebook file, so you can save and submit safely. The strip at the end removes invisible spaces that sneak in when you copy on Windows." | 0:45 |
| 3 | Run the cell, the prompt appears, paste the throwaway key, press Enter. Point out that nothing is displayed | "I just pasted my key. Nothing shows, and that is exactly what we want." | 0:20 |
| 4 | Run the lab setup cell and the API check cell from any course lab; the line `deepseek ready | model: deepseek-flash | status: connected` appears | "Now the normal lab cells run. This connected line is your proof everything works." | 0:30 |
| 5 | Show, without executing, the shell profile alternative from the page (the two export lines with the placeholder `sk-PASTE-YOUR-KEY-HERE`) | "If typing the key each session annoys you, put these two lines in your shell profile once, with your real key in place of the placeholder, and every lab finds them automatically." | 0:30 |
| 6 | Show the OpenAI note at the bottom of the page for two seconds, do not run anything | "If you use OpenAI instead, it is even shorter: one key, no provider line. Same hidden prompt pattern." | 0:20 |
| 7 | End card per course video convention | "Set the key, run the check, start the lab." | 0:10 |

Do NOT in video 1: show a real key anywhere, demo the OpenAI variant (the two
second glance at the note is enough), or wander into Colab.

## Video 2: When the key does not work (target 3:30)

Each failure is staged first, so the student sees their exact error text.

| # | On screen | Say roughly | Time |
|---|---|---|---|
| 1 | Title cell "Four errors, four fixes" | "Four things go wrong with keys. Here is each one, with its fix." | 0:10 |
| 2 | Fresh kernel. Run the lab setup cell WITHOUT running the key cell; the key prompt or a not found error appears | "Error one: key not found. The key cell simply has not run in this session. Run the key cell first, then the setup cell. Order matters." | 0:40 |
| 3 | Simulate a padded key: set `os.environ["DEEPSEEK_API_KEY"] = "sk-demo "` with a visible trailing space, run a call, show the 401. Then rerun through the getpass cell with strip | "Error two: the key is right but the provider says invalid. That is an invisible space or line ending from copy paste, very common on Windows. Our key cell strips it automatically." | 0:50 |
| 4 | Kernel menu, Restart kernel. Re run a lab cell, key gone again | "Error three: it worked all morning, then died. A kernel restart wipes everything the key cell set. Not a bug: run the key cell again, or use the shell profile option and it survives restarts." | 0:40 |
| 5 | Show a first cell setting `LLM_PROVIDER` AFTER the setup cell already ran; the check still says OpenAI. Then restart, run provider cell first, check now says deepseek ready. Use the throwaway DeepSeek key or cut before any prompt entry | "Error four: the provider line must run before the setup cell. Set it in the very first cell, restart, run top to bottom." | 0:50 |
| 6 | The never do box from the Canvas page on screen | "And never print the key, never hardcode it in a cell, never push output that contains it. If a key ever leaks, revoke it on the dashboard and make a new one." | 0:20 |

Do NOT in video 2: display a real key while staging the padded key demo (use
the literal `sk-demo` string), show your provider dashboard billing page, or
show shell history containing a real export line.

## Delivery

Upload to the host MD confirms, send MD the link and the duration of each
video. MD places them on the Canvas page; Saqar does not post to Canvas.
