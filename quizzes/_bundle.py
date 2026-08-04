import re, os
QDIR = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI/quizzes")
WEB = os.path.join(QDIR, "website")
os.makedirs(WEB, exist_ok=True)

CSS = open(os.path.join(QDIR, "quiz_engine.css")).read()
JS = open(os.path.join(QDIR, "quiz_engine.js")).read()
MODS = ["M01","M02","M03","M04","M05","M06","M08","M09","M10","M11","M12","M13"]

FONT = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'

def title_of(mod):
    src = open(os.path.join(QDIR, "data", f"{mod}_quiz.js")).read()
    m = re.search(r'title:\s*"([^"]+)"', src)
    return (m.group(1) if m else mod), src

def standalone(mod, review):
    title, data = title_of(mod)
    kind = "Answer key (colleagues)" if review else "Student quiz"
    doc = f"""<!--
  DADS 5250 Module Quiz, {mod}: {title}  ({kind})
  SELF-CONTAINED: this single .html file needs no other files (it only loads the Outfit web font from Google).
  HOW TO ADD IT TO THE WEBSITE, pick one:
    1) Upload this file and embed it:  <iframe src="{mod}_Quiz.html" style="width:100%;height:940px;border:0"></iframe>
    2) Or link to it directly from the module page.
  Two versions exist per module: {mod}_Quiz.html (student, answers hidden) and {mod}_Review.html (answer key, answers shown).
  Everything runs in the browser. No data is sent anywhere; the student's answers stay on their device.
-->"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{mod} {'Answer Key' if review else 'Quiz'}, {title}</title>
{doc}
{FONT}
<style>
{CSS}
</style>
</head>
<body>
<div class="container">
  <div class="quiz-header" id="quiz-header"></div>
  <div id="quiz-root"></div>
</div>
<script>
{data}
window.REVIEW = {str(review).lower()};
</script>
<script>
{JS}
</script>
</body>
</html>
"""

for mod in MODS:
    open(os.path.join(WEB, f"{mod}_Quiz.html"), "w").write(standalone(mod, False))
    open(os.path.join(WEB, f"{mod}_Review.html"), "w").write(standalone(mod, True))
print("wrote", len(MODS)*2, "self-contained files to website/")

# ---- documented how-to page with per-module preview + copy snippet ----
cards = ""
for mod in MODS:
    title, _ = title_of(mod)
    snippet = f'&lt;iframe src="{mod}_Quiz.html" style="width:100%;height:940px;border:0"&gt;&lt;/iframe&gt;'
    cards += f"""
  <section class="mcard">
    <div class="mhead"><span class="mcode">{mod}</span><span class="mtitle">{title}</span>
      <span class="mlinks"><a href="{mod}_Quiz.html" target="_blank">student</a> &middot; <a href="{mod}_Review.html" target="_blank">answer key</a></span></div>
    <p class="mdoc">Embed snippet to paste into the website:</p>
    <pre class="snip">{snippet}</pre>
    <iframe class="prev" src="{mod}_Quiz.html" title="{mod} preview" loading="lazy"></iframe>
  </section>"""

howto = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DADS 5250 Quizzes, how to add them to the website</title>
{FONT}
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Outfit',system-ui,sans-serif;background:#F0F4FA;color:#1e293b;padding:40px 20px}}
.wrap{{max-width:900px;margin:0 auto}}
h1{{font-size:1.9rem;font-weight:700}}
.lead{{color:#475569;margin:8px 0 22px;line-height:1.6}}
.steps{{background:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.6);border-radius:16px;padding:20px 24px;margin-bottom:30px;box-shadow:0 8px 32px rgba(37,99,235,0.08)}}
.steps h2{{font-size:1.05rem;color:#2563EB;margin-bottom:10px}}
.steps ol{{margin-left:18px;line-height:1.8;color:#1e293b}}
.steps code{{background:rgba(37,99,235,0.08);padding:2px 6px;border-radius:6px;font-family:ui-monospace,Menlo,monospace;font-size:0.9em}}
.mcard{{background:rgba(255,255,255,0.55);border:1px solid rgba(255,255,255,0.6);border-radius:16px;padding:20px 22px;margin-bottom:26px;box-shadow:0 8px 32px rgba(37,99,235,0.06)}}
.mhead{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px}}
.mcode{{font-weight:700;color:#2563EB}}
.mtitle{{font-weight:600}}
.mlinks{{margin-left:auto;font-size:0.9rem}}
.mlinks a{{color:#2563EB;font-weight:600;text-decoration:none}}
.mdoc{{color:#475569;font-size:0.9rem;margin-bottom:6px}}
.snip{{background:#0f172a;color:#e2e8f0;border-radius:10px;padding:12px 14px;font-family:ui-monospace,Menlo,monospace;font-size:0.85rem;overflow-x:auto;margin-bottom:14px}}
.prev{{width:100%;height:620px;border:1px solid #e2e8f0;border-radius:12px;background:#F0F4FA}}
</style></head><body><div class="wrap">
<h1>DADS 5250 Quizzes, how to add them to the website</h1>
<p class="lead">Each module below has a self-contained quiz. Every file is standalone: it needs no other files and only loads the Outfit web font. Answers are checked in the browser and nothing is sent anywhere. There are two versions per module: the student quiz (answers hidden until answered) and the answer key (all answers and explanations shown, for reviewers).</p>
<div class="steps"><h2>To add a module quiz to the website</h2>
<ol>
<li>Upload that module's <code>MXX_Quiz.html</code> file (from the <code>website/</code> folder) to the site.</li>
<li>On the module's page, paste the embed snippet shown under that module (an <code>iframe</code>).</li>
<li>That is all. To let a reviewer see the correct answers, use <code>MXX_Review.html</code> instead.</li>
</ol></div>
{cards}
</div></body></html>"""
open(os.path.join(WEB, "HOW_TO_ADD.html"), "w").write(howto)
print("wrote website/HOW_TO_ADD.html")
