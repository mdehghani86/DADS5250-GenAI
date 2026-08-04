import os, re, zipfile
QDIR = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI/quizzes")
MODS = ["M01","M02","M03","M04","M05","M06","M08","M09","M10","M11","M12","M13"]
FONT = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'

def title_of(mod):
    src = open(os.path.join(QDIR, "data", f"{mod}_quiz.js")).read()
    m = re.search(r'title:\s*"([^"]+)"', src)
    return m.group(1) if m else mod

# ---- 1. regenerate the 12 student + review wrappers with the Canvas link ----
def wrapper(mod, review):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{mod} {'Answer Key' if review else 'Quiz'}, {title_of(mod)}</title>
{FONT}
<link rel="stylesheet" href="quiz_engine.css">
</head>
<body>
<div class="container">
  <div class="quiz-header" id="quiz-header"></div>
  <div id="quiz-root"></div>
</div>
<script src="data/{mod}_quiz.js"></script>
<script>window.REVIEW = {str(review).lower()}; window.CANVAS_ZIP = 'canvas/{mod}_Canvas.zip';</script>
<script src="quiz_engine.js"></script>
</body>
</html>
"""
for mod in MODS:
    open(os.path.join(QDIR, f"{mod}_Quiz.html"), "w").write(wrapper(mod, False))
    open(os.path.join(QDIR, f"{mod}_Review.html"), "w").write(wrapper(mod, True))
print("regenerated 24 wrappers with Canvas download link")

# ---- 2. REVIEW_ALL.html with a Canvas download column ----
rows = ""
for mod in MODS:
    rows += (f'<tr><td class="mod">{mod}</td><td>{title_of(mod)}</td>'
             f'<td><a href="{mod}_Quiz.html">Student quiz</a></td>'
             f'<td><a href="{mod}_Review.html">Answer key</a></td>'
             f'<td><a href="canvas/{mod}_Canvas.zip" download>Canvas .zip</a></td></tr>\n')
open(os.path.join(QDIR, "REVIEW_ALL.html"), "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DADS 5250 Quizzes, review index</title>{FONT}
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Outfit',system-ui,sans-serif;background:#F0F4FA;color:#1e293b;padding:48px 24px}}
.wrap{{max-width:900px;margin:0 auto}} h1{{font-size:1.9rem;font-weight:700}}
p.sub{{color:#475569;margin:6px 0 20px;line-height:1.6}}
.note{{background:rgba(37,99,235,0.08);border:1px solid rgba(37,99,235,0.2);border-radius:12px;padding:12px 16px;margin-bottom:24px;font-size:0.92rem}}
.note a{{color:#2563EB;font-weight:600}}
table{{width:100%;border-collapse:collapse;background:rgba(255,255,255,0.55);border:1px solid rgba(255,255,255,0.6);border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(37,99,235,0.08)}}
th,td{{text-align:left;padding:13px 16px;border-bottom:1px solid rgba(37,99,235,0.08);font-size:0.96rem}}
th{{font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#2563EB;font-weight:600}}
td.mod{{font-weight:700;color:#2563EB}} a{{color:#2563EB;font-weight:600;text-decoration:none}} a:hover{{text-decoration:underline}}
tr:last-child td{{border-bottom:0}}
</style></head><body><div class="wrap">
<h1>DADS 5250 Quizzes</h1>
<p class="sub">Each module has a 5-question quiz. The answer key shows every question with the correct answer and all per-option explanations. The student quiz keeps answers hidden until answered. The Canvas column downloads a QTI .zip you can import into a Canvas course.</p>
<div class="note">To add a quiz to Canvas: download its <b>Canvas .zip</b>, then in the Canvas course go to <b>Settings &rarr; Import Course Content &rarr; QTI .zip file</b> and upload it. Full steps: <a href="CANVAS_IMPORT.html">CANVAS_IMPORT.html</a>.</div>
<table><thead><tr><th>Module</th><th>Title</th><th>Student</th><th>Review</th><th>Canvas</th></tr></thead><tbody>
{rows}</tbody></table></div></body></html>""")
print("wrote REVIEW_ALL.html with Canvas column")

# ---- 3. import documentation ----
open(os.path.join(QDIR, "CANVAS_IMPORT.html"), "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Importing the quizzes into Canvas</title>{FONT}
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Outfit',system-ui,sans-serif;background:#F0F4FA;color:#1e293b;padding:48px 24px;line-height:1.65}}
.wrap{{max-width:760px;margin:0 auto}}h1{{font-size:1.8rem;font-weight:700;margin-bottom:8px}}h2{{font-size:1.15rem;color:#2563EB;margin:26px 0 8px}}
ol{{margin:8px 0 8px 20px}}li{{margin-bottom:8px}}code{{background:rgba(37,99,235,0.08);padding:2px 6px;border-radius:6px;font-family:ui-monospace,Menlo,monospace;font-size:0.9em}}
.card{{background:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.6);border-radius:16px;padding:22px 26px;box-shadow:0 8px 32px rgba(37,99,235,0.08)}}
.small{{color:#475569;font-size:0.92rem}}</style></head><body><div class="wrap"><div class="card">
<h1>Importing a module quiz into Canvas</h1>
<p class="small">Each module has a QTI 1.2 package (a .zip) that Canvas Classic Quizzes can import directly.</p>
<h2>Two-step import</h2>
<ol>
<li>Download the module's package: click <b>Download for Canvas (QTI .zip)</b> on the quiz page, or take <code>quizzes/canvas/MXX_Canvas.zip</code>.</li>
<li>In the Canvas course, open <b>Settings</b> &rarr; <b>Import Course Content</b>. For <b>Content Type</b> choose <b>QTI .zip file</b>, select the downloaded .zip, and click <b>Import</b>.</li>
</ol>
<p class="small">When the import job finishes, the quiz appears under <b>Quizzes</b> (Classic). Open it to review before publishing.</p>
<h2>What is included</h2>
<ol>
<li>All 5 questions with their options and the correct answer(s).</li>
<li><b>Per-answer feedback</b>: the comment for each option (why the correct one is right, and why each wrong one is wrong) imports as Canvas answer comments.</li>
<li><b>Points</b>: easy = 1, medium = 2, hard = 3, so each module quiz totals 10 points.</li>
<li><b>Graphic questions</b>: the diagram is rendered to a PNG and embedded in the question, and the PNG is also shipped inside the .zip.</li>
</ol>
<h2>Question type mapping</h2>
<p class="small">Multiple choice, practical, coding, and graphic questions import as <b>Multiple Choice</b>. Multiple-select imports as <b>Multiple Answers</b>. True/False and Fill-in import as their Canvas equivalents. Ordering questions import as <b>Multiple Choice</b> (pick the correct sequence), since Canvas Classic has no native ordering type.</p>
<h2>If a diagram image does not appear</h2>
<p class="small">Some Canvas instances handle imported images differently. If a diagram is missing after import, the PNG is inside the .zip (named <code>MXX_qN.png</code>) and can be inserted into the question with the Canvas image tool.</p>
</div></div></body></html>""")
print("wrote CANVAS_IMPORT.html")

# ---- 4. structural dry-check of every QTI package ----
print("\n=== QTI STRUCTURAL DRY-CHECK ===")
allok = True
for mod in MODS:
    z = os.path.join(QDIR, "canvas", f"{mod}_Canvas.zip")
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
        has_manifest = "imsmanifest.xml" in names
        qname = f"{mod}_quiz.xml"
        xml = zf.read(qname).decode() if qname in names else ""
    items = xml.count("<item ")
    checks = {
        "manifest": has_manifest,
        "questestinterop": "<questestinterop" in xml,
        "assessment": "<assessment " in xml,
        "5 items": items == 5,
        "question_type on all": xml.count("<fieldlabel>question_type</fieldlabel>") == 5,
        "points on all": xml.count("points_possible") == 5,
        "scoring (SCORE=100) on all": xml.count('varname="SCORE">100') == 5,
        "per-answer feedback present": "itemfeedback" in xml,
    }
    bad = [k for k, v in checks.items() if not v]
    allok = allok and not bad
    print(f"{mod}: items={items}  " + ("OK" if not bad else "ISSUES: " + ", ".join(bad)))
print("\nALL PACKAGES PASS" if allok else "\nSOME PACKAGES HAVE ISSUES")
