import re, os
BASE = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI")
QDIR = os.path.join(BASE, "quizzes")

MODS = [
    ("M01", "scripts/M01_LLM_APIs/M01_Module.html"),
    ("M02", "scripts/M02_AI_in_Action/M02_Module.html"),
    ("M03", "scripts/M03_Prompt_Structured_FunctionCalling/M03_Module.html"),
    ("M04", "scripts/M04_LangChain/M04_Module.html"),
    ("M05", "scripts/M05_RAG/M05_Module.html"),
    ("M06", "scripts/M06_Agents_OpenAI/M06_Module.html"),
    ("M08", "scripts/M08_MultiAgent/M08_Module.html"),
    ("M09", "scripts/M09_Frontend/M09_Module.html"),
    ("M10", "scripts/M10_Vision_Eval/M10_Module.html"),
    ("M11", "scripts/M11_ClaudeCode/M11_Module.html"),
    ("M12", "scripts/M12_AI_Platforms/M12_Module.html"),
    ("M13", "scripts/M13_Ethics_Safety/M13_Module.html"),
]

def title_of(mod):
    src = open(os.path.join(QDIR, "data", f"{mod}_quiz.js")).read()
    m = re.search(r'title:\s*"([^"]+)"', src)
    return m.group(1) if m else mod

# ---- 1. REVIEW_ALL.html index ----
rows = ""
for mod, _ in MODS:
    t = title_of(mod)
    rows += (f'<tr><td class="mod">{mod}</td><td>{t}</td>'
             f'<td><a href="{mod}_Quiz.html">Student quiz</a></td>'
             f'<td><a href="{mod}_Review.html">Answer key</a></td></tr>\n')
index = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DADS 5250 Quizzes, colleague review index</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Outfit',system-ui,sans-serif;background:#F0F4FA;color:#1e293b;padding:48px 24px}}
.wrap{{max-width:820px;margin:0 auto}}
h1{{font-size:1.9rem;font-weight:700}}
p.sub{{color:#475569;margin:6px 0 28px}}
table{{width:100%;border-collapse:collapse;background:rgba(255,255,255,0.55);border:1px solid rgba(255,255,255,0.6);border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(37,99,235,0.08)}}
th,td{{text-align:left;padding:14px 18px;border-bottom:1px solid rgba(37,99,235,0.08);font-size:0.98rem}}
th{{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em;color:#2563EB;font-weight:600}}
td.mod{{font-weight:700;color:#2563EB}}
a{{color:#2563EB;font-weight:600;text-decoration:none}}
a:hover{{text-decoration:underline}}
tr:last-child td{{border-bottom:0}}
</style></head><body><div class="wrap">
<h1>DADS 5250 Quizzes</h1>
<p class="sub">Colleague review index. Each module has a 5-question quiz. The answer key shows every question with the correct answer and all explanations. The student quiz keeps answers hidden until answered.</p>
<table><thead><tr><th>Module</th><th>Title</th><th>Student</th><th>Review</th></tr></thead><tbody>
{rows}</tbody></table>
</div></body></html>"""
open(os.path.join(QDIR, "REVIEW_ALL.html"), "w").write(index)
print("wrote REVIEW_ALL.html")

# ---- 2. embed a quiz section into each module page (iframe isolates CSS) ----
def embed(mod):
    return f"""
<!-- DADS-QUIZ-EMBED -->
<section id="module-quiz-embed" style="max-width:900px;margin:48px auto;padding:0 20px;font-family:'Outfit',system-ui,sans-serif">
  <h2 style="font-size:1.5rem;font-weight:700;color:#1e293b;margin:0 0 6px">Module quiz</h2>
  <p style="color:#475569;margin:0 0 16px">Five questions on this module. Answers are checked instantly with explanations.</p>
  <iframe src="../../quizzes/{mod}_Quiz.html" title="{mod} quiz" loading="lazy" style="width:100%;height:940px;border:1px solid #e2e8f0;border-radius:16px;background:#F0F4FA"></iframe>
  <p style="margin-top:12px;font-size:0.95rem;color:#475569"><a href="../../quizzes/{mod}_Quiz.html" target="_blank" style="color:#2563EB;font-weight:600">Open full screen</a> &nbsp;&middot;&nbsp; <a href="../../quizzes/{mod}_Review.html" target="_blank" style="color:#2563EB;font-weight:600">Answer key (for colleagues)</a></p>
</section>
<!-- /DADS-QUIZ-EMBED -->
"""

done = []
for mod, rel in MODS:
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print("MISSING module page:", rel); continue
    html = open(path).read()
    if "DADS-QUIZ-EMBED" in html:
        # replace existing embed (idempotent)
        html = re.sub(r"\n?<!-- DADS-QUIZ-EMBED -->.*?<!-- /DADS-QUIZ-EMBED -->\n?", "", html, flags=re.S)
    idx = html.rfind("</body>")
    if idx == -1:
        html = html + embed(mod)
    else:
        html = html[:idx] + embed(mod) + html[idx:]
    open(path, "w").write(html)
    done.append(mod)
print("embedded quiz into module pages:", ", ".join(done))
