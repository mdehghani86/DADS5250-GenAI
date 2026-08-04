import os, re
BASE = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI")
QDIR = os.path.join(BASE, "quizzes"); WEB = os.path.join(QDIR, "website")
os.makedirs(WEB, exist_ok=True)
CSS = open(os.path.join(QDIR, "quiz_engine.css")).read()
JS = open(os.path.join(QDIR, "quiz_engine.js")).read()
FONT = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
MODS = [
    ("M01","scripts/M01_LLM_APIs/M01_Module.html"),
    ("M02","scripts/M02_AI_in_Action/M02_Module.html"),
    ("M03","scripts/M03_Prompt_Structured_FunctionCalling/M03_Module.html"),
    ("M04","scripts/M04_LangChain/M04_Module.html"),
    ("M05","scripts/M05_RAG/M05_Module.html"),
    ("M06","scripts/M06_Agents_OpenAI/M06_Module.html"),
    ("M08","scripts/M08_MultiAgent/M08_Module.html"),
    ("M09","scripts/M09_Frontend/M09_Module.html"),
    ("M10","scripts/M10_Vision_Eval/M10_Module.html"),
    ("M11","scripts/M11_ClaudeCode/M11_Module.html"),
    ("M12","scripts/M12_AI_Platforms/M12_Module.html"),
    ("M13","scripts/M13_Ethics_Safety/M13_Module.html"),
]
def title_of(mod):
    src = open(os.path.join(QDIR, "data", f"{mod}_quiz.js")).read()
    m = re.search(r'title:\s*"([^"]+)"', src); return m.group(1) if m else mod

# ---- 1. single quiz page per module (external engine) + remove Review pages ----
for mod, _ in MODS:
    open(os.path.join(QDIR, f"{mod}_Quiz.html"), "w").write(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{mod} Quiz, {title_of(mod)}</title>
{FONT}<link rel="stylesheet" href="quiz_engine.css"></head><body>
<div class="container"><div class="quiz-header" id="quiz-header"></div><div id="quiz-root"></div></div>
<script src="data/{mod}_quiz.js"></script>
<script>window.CANVAS_ZIP = 'canvas/{mod}_Canvas.zip';</script>
<script src="quiz_engine.js"></script></body></html>""")
    for junk in (os.path.join(QDIR, f"{mod}_Review.html"), os.path.join(WEB, f"{mod}_Review.html")):
        if os.path.exists(junk): os.remove(junk)
    # self-contained bundle
    data = open(os.path.join(QDIR, "data", f"{mod}_quiz.js")).read()
    open(os.path.join(WEB, f"{mod}_Quiz.html"), "w").write(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{mod} Quiz, {title_of(mod)}</title>
<!-- Self-contained single file. Development / review view: shows every question with the correct
     answer and all per-option feedback. Not a student-testing view. Only loads the Outfit web font. -->
{FONT}<style>{CSS}</style></head><body>
<div class="container"><div class="quiz-header" id="quiz-header"></div><div id="quiz-root"></div></div>
<script>{data}
window.CANVAS_ZIP = '../canvas/{mod}_Canvas.zip';</script>
<script>{JS}</script></body></html>""")
print("wrote single quiz page + bundle per module; removed Review pages")

# ---- 2. index (REVIEW_ALL) ----
rows = "".join(f'<tr><td class="mod">{m}</td><td>{title_of(m)}</td><td><a href="{m}_Quiz.html">Open quiz</a></td><td><a href="canvas/{m}_Canvas.zip" download>Canvas .zip</a></td></tr>\n' for m,_ in MODS)
open(os.path.join(QDIR, "REVIEW_ALL.html"), "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>DADS 5250 Quizzes</title>{FONT}
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Outfit',system-ui,sans-serif;background:#F0F4FA;color:#1e293b;padding:48px 24px}}
.wrap{{max-width:900px;margin:0 auto}}h1{{font-size:1.9rem;font-weight:700}}p.sub{{color:#475569;margin:6px 0 20px;line-height:1.6}}
.note{{background:rgba(37,99,235,0.08);border:1px solid rgba(37,99,235,0.2);border-radius:12px;padding:12px 16px;margin-bottom:24px;font-size:0.92rem}}.note a{{color:#2563EB;font-weight:600}}
table{{width:100%;border-collapse:collapse;background:rgba(255,255,255,0.55);border:1px solid rgba(255,255,255,0.6);border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(37,99,235,0.08)}}
th,td{{text-align:left;padding:13px 16px;border-bottom:1px solid rgba(37,99,235,0.08);font-size:0.96rem}}th{{font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#2563EB;font-weight:600}}
td.mod{{font-weight:700;color:#2563EB}}a{{color:#2563EB;font-weight:600;text-decoration:none}}a:hover{{text-decoration:underline}}tr:last-child td{{border-bottom:0}}</style></head><body><div class="wrap">
<h1>DADS 5250 Quizzes</h1>
<p class="sub">Development and review build. Each quiz page shows all 5 questions fully expanded: the correct answer is marked and every per-option feedback comment is visible. A copy button sits next to every field. This is for colleague review, not student testing.</p>
<div class="note">To add a quiz to Canvas: download its <b>Canvas .zip</b>, then in the Canvas course go to <b>Settings &rarr; Import Course Content &rarr; QTI .zip file</b> and upload it. Full steps: <a href="CANVAS_IMPORT.html">CANVAS_IMPORT.html</a>.</div>
<table><thead><tr><th>Module</th><th>Title</th><th>Quiz</th><th>Canvas</th></tr></thead><tbody>
{rows}</tbody></table></div></body></html>""")
print("wrote REVIEW_ALL.html (single-view index)")

# ---- 3. re-embed single quiz into each module page ----
def embed(mod):
    return f"""
<!-- DADS-QUIZ-EMBED -->
<section id="module-quiz-embed" style="max-width:900px;margin:48px auto;padding:0 20px;font-family:'Outfit',system-ui,sans-serif">
  <h2 style="font-size:1.5rem;font-weight:700;color:#1e293b;margin:0 0 6px">Module quiz (review build)</h2>
  <p style="color:#475569;margin:0 0 16px">All questions with correct answers and per-option feedback. Use the Download for Canvas button to import into a Canvas course.</p>
  <iframe src="../../quizzes/{mod}_Quiz.html" title="{mod} quiz" loading="lazy" style="width:100%;height:1000px;border:1px solid #e2e8f0;border-radius:16px;background:#F0F4FA"></iframe>
  <p style="margin-top:12px;font-size:0.95rem"><a href="../../quizzes/{mod}_Quiz.html" target="_blank" style="color:#2563EB;font-weight:600">Open full screen</a> &nbsp;&middot;&nbsp; <a href="../../quizzes/canvas/{mod}_Canvas.zip" download style="color:#2563EB;font-weight:600">Download for Canvas</a></p>
</section>
<!-- /DADS-QUIZ-EMBED -->
"""
for mod, rel in MODS:
    p = os.path.join(BASE, rel)
    if not os.path.exists(p): print("MISSING", rel); continue
    h = open(p).read()
    h = re.sub(r"\n?<!-- DADS-QUIZ-EMBED -->.*?<!-- /DADS-QUIZ-EMBED -->\n?", "", h, flags=re.S)
    idx = h.rfind("</body>")
    h = (h[:idx] + embed(mod) + h[idx:]) if idx != -1 else (h + embed(mod))
    open(p, "w").write(h)
print("re-embedded single quiz into 12 module pages")
