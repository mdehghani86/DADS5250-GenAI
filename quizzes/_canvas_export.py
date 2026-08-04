#!/usr/bin/env python3
"""Generate a Canvas-importable QTI 1.2 .zip per module from the quiz data.

Canvas Classic quizzes accept a QTI 1.2 package (imsmanifest.xml + a
questestinterop XML) using only legacy 1.2 elements. This builder maps:
  mc / coding / practical / graphic -> multiple_choice_question
  multi                             -> multiple_answers_question
  tf                                -> true_false_question
  fill                              -> short_answer_question
  order                             -> multiple_choice_question (correct sequence + generated distractor orderings)
Per-answer feedback (the option explanations) is included via <itemfeedback> +
<displayfeedback>. Points: easy=1, medium=2, hard=3. Graphic questions render
their SVG to PNG, embedded in the question as a $IMS-CC-FILEBASE$ reference and
also shipped in the zip.
"""
import json, os, re, zipfile, subprocess, hashlib, html
from xml.sax.saxutils import escape

BASE = os.path.expanduser("~/Library/CloudStorage/Dropbox/5_Courses/DADS5250-GenAI/quizzes")
OUT = os.path.join(BASE, "canvas")
IMG = os.path.join(BASE, "canvas", "_img")
os.makedirs(OUT, exist_ok=True); os.makedirs(IMG, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
POINTS = {"easy": 1, "medium": 2, "hard": 3}

quizzes = json.load(open("/tmp/quizzes.json"))

def strip(s):  # plain text from lightweight HTML
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s))).strip()

def attr(s):  # attribute-safe (escape & < > and quotes)
    return escape(str(s), {'"': "&quot;", "'": "&apos;"})

def svg_to_png(svg, name):
    """Render an SVG string to a PNG via headless Chrome. Returns the png path."""
    htmlf = os.path.join(IMG, name + ".html")
    pngf = os.path.join(IMG, name + ".png")
    open(htmlf, "w").write(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>*{margin:0;padding:0}"
        "body{background:#fff}svg{display:block;width:640px;height:260px}</style></head><body>"
        + svg + "</body></html>")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--default-background-color=FFFFFFFF",
                    "--window-size=640,260", f"--screenshot={pngf}", f"file://{htmlf}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=40)
    return pngf if os.path.exists(pngf) else None

def cdata(s):
    return "<![CDATA[" + str(s).replace("]]>", "]]]]><![CDATA[>") + "]]>"

def question_html(q, img_ref):
    h = "<div>" + q["prompt"] + "</div>"
    if q.get("code"):
        h += "<pre style='background:#0f172a;color:#e2e8f0;padding:12px;border-radius:8px;white-space:pre;font-family:monospace'>" + html.escape(q["code"]) + "</pre>"
    if img_ref:
        h += f"<p><img src=\"{img_ref}\" alt=\"diagram\" width=\"620\"></p>"
    return h

def item_choice(qid, q, img_ref, answers, correct_ids, multiple=False):
    """answers: list of (ident, html_text, feedback). correct_ids: set of idents."""
    qtype = "multiple_answers_question" if multiple else ("true_false_question" if q.get("_tf") else "multiple_choice_question")
    pts = POINTS.get(q.get("difficulty"), 1)
    labels = "".join(
        f'<response_label ident="{aid}"><material><mattext texttype="text/html">{cdata(txt)}</mattext></material></response_label>'
        for aid, txt, _ in answers)
    card = "Multiple" if multiple else "Single"
    # scoring
    if multiple:
        conds = "".join(f'<varequal respident="response1">{aid}</varequal>' if aid in correct_ids
                        else f'<not><varequal respident="response1">{aid}</varequal></not>' for aid, _, _ in answers)
        score = f'<respcondition continue="No"><conditionvar><and>{conds}</and></conditionvar><setvar action="Set" varname="SCORE">100</setvar></respcondition>'
    else:
        cid = next(iter(correct_ids))
        score = f'<respcondition continue="No"><conditionvar><varequal respident="response1">{cid}</varequal></conditionvar><setvar action="Set" varname="SCORE">100</setvar></respcondition>'
    # per-answer feedback
    fb_conds, fb_blocks = "", ""
    for aid, _, fb in answers:
        if not fb: continue
        fb_conds += f'<respcondition continue="Yes"><conditionvar><varequal respident="response1">{aid}</varequal></conditionvar><displayfeedback feedbacktype="Response" linkrefid="{aid}_fb"/></respcondition>'
        fb_blocks += f'<itemfeedback ident="{aid}_fb"><flow_mat><material><mattext texttype="text/html">{cdata(fb)}</mattext></material></flow_mat></itemfeedback>'
    return f"""    <item ident="{qid}" title="{attr(strip(q['prompt'])[:60])}">
      <itemmetadata><qtimetadata>
        <qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>{qtype}</fieldentry></qtimetadatafield>
        <qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>{pts}.0</fieldentry></qtimetadatafield>
      </qtimetadata></itemmetadata>
      <presentation>
        <material><mattext texttype="text/html">{cdata(question_html(q, img_ref))}</mattext></material>
        <response_lid ident="response1" rcardinality="{card}"><render_choice>{labels}</render_choice></response_lid>
      </presentation>
      <resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
        {fb_conds}{score}
      </resprocessing>
      {fb_blocks}
    </item>"""

def item_fill(qid, q):
    pts = POINTS.get(q.get("difficulty"), 1)
    ors = "".join(f'<varequal respident="response1">{escape(str(a))}</varequal>' for a in q["accept"])
    fb = f'<respcondition continue="Yes"><conditionvar><other/></conditionvar><displayfeedback feedbacktype="Response" linkrefid="general_fb"/></respcondition>' if q.get("explanation") else ""
    fbb = f'<itemfeedback ident="general_fb"><flow_mat><material><mattext texttype="text/html">{cdata(q.get("explanation",""))}</mattext></material></flow_mat></itemfeedback>' if q.get("explanation") else ""
    return f"""    <item ident="{qid}" title="{attr(strip(q['prompt'])[:60])}">
      <itemmetadata><qtimetadata>
        <qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>short_answer_question</fieldentry></qtimetadatafield>
        <qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>{pts}.0</fieldentry></qtimetadatafield>
      </qtimetadata></itemmetadata>
      <presentation>
        <material><mattext texttype="text/html">{cdata(question_html(q, None))}</mattext></material>
        <response_str ident="response1" rcardinality="Single"><render_fib><response_label ident="answer1"/></render_fib></response_str>
      </presentation>
      <resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
        {fb}
        <respcondition continue="No"><conditionvar><or>{ors}</or></conditionvar><setvar action="Set" varname="SCORE">100</setvar></respcondition>
      </resprocessing>
      {fbb}
    </item>"""

def build_item(mod, i, q):
    qid = f"{mod}_q{i+1}"
    img_ref = None
    if q.get("diagram"):
        png = svg_to_png(q["diagram"], qid)
        if png:
            img_ref = "$IMS-CC-FILEBASE$/" + qid + ".png"
    t = q["type"]
    if t == "mc":
        answers = [(f"{qid}_a{j}", o["text"], o.get("explanation")) for j, o in enumerate(q["options"])]
        return qid, img_ref, item_choice(qid, q, img_ref, answers, {f"{qid}_a{q['correctIndex']}"})
    if t == "multi":
        answers = [(f"{qid}_a{j}", o["text"], o.get("explanation")) for j, o in enumerate(q["options"])]
        correct = {f"{qid}_a{j}" for j in q["correctIndices"]}
        return qid, img_ref, item_choice(qid, q, img_ref, answers, correct, multiple=True)
    if t == "tf":
        q["_tf"] = True
        answers = [(f"{qid}_true", "True", None), (f"{qid}_false", "False", None)]
        correct = {f"{qid}_" + ("true" if q["correctAnswer"] else "false")}
        # attach single explanation to the correct answer feedback
        answers = [(aid, txt, q.get("explanation") if aid in correct else "") for aid, txt, _ in answers]
        return qid, img_ref, item_choice(qid, q, img_ref, answers, correct)
    if t == "fill":
        return qid, None, item_fill(qid, q)
    if t == "order":
        seq = [q["items"][q["correctOrder"].index(p)] for p in range(len(q["items"]))]
        correct_txt = " -> ".join(seq)
        # generate 3 distractor orderings
        import itertools
        perms = [list(p) for p in itertools.permutations(seq)]
        distract = [pp for pp in perms if pp != seq]
        picks = [distract[0], distract[len(distract)//2], distract[-1]]
        opts = [correct_txt] + [" -> ".join(p) for p in picks]
        q2 = dict(q); q2["prompt"] = q["prompt"] + " <em>(choose the correct order)</em>"
        answers = [(f"{qid}_a{j}", txt, (q.get("explanation") if j == 0 else "This ordering is incorrect. Review the correct sequence in the explanation of the right answer.")) for j, txt in enumerate(opts)]
        return qid, img_ref, item_choice(qid, q2, img_ref, answers, {f"{qid}_a0"})
    return qid, None, ""

def build_module(mod):
    quiz = quizzes[mod]
    title = quiz["meta"]["title"]
    items, imgs = [], []
    total = 0
    for i, q in enumerate(quiz["questions"]):
        qid, img_ref, xml = build_item(mod, i, q)
        items.append(xml); total += POINTS.get(q.get("difficulty"), 1)
        if img_ref:
            imgs.append(qid + ".png")
    asmt_id = f"{mod}_assessment"
    qti = f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">
  <assessment ident="{asmt_id}" title="{escape(mod + ': ' + title)}">
    <qtimetadata><qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield></qtimetadata>
    <section ident="root_section">
{chr(10).join(items)}
    </section>
  </assessment>
</questestinterop>"""
    # manifest
    img_res = "".join(
        f'    <resource identifier="res_{os.path.splitext(im)[0]}" type="webcontent" href="{im}"><file href="{im}"/></resource>\n'
        for im in imgs)
    manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{mod}_manifest" xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
  xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>
  <organizations/>
  <resources>
    <resource identifier="{asmt_id}" type="imsqti_xmlv1p2/imscc_xmlv1p1/assessment" href="{mod}_quiz.xml">
      <file href="{mod}_quiz.xml"/>
    </resource>
{img_res}  </resources>
</manifest>"""
    zpath = os.path.join(OUT, f"{mod}_Canvas.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        z.writestr(f"{mod}_quiz.xml", qti)
        for im in imgs:
            z.write(os.path.join(IMG, im), im)
    return zpath, total, len(imgs), qti

if __name__ == "__main__":
    import xml.dom.minidom as MD
    print(f"{'module':6} {'points':7} {'images':7} {'zip'}")
    for mod in quizzes:
        zpath, total, nimg, qti = build_module(mod)
        try:
            MD.parseString(qti); ok = "valid-xml"
        except Exception as e:
            ok = "XML ERROR: " + str(e)
        print(f"{mod:6} {total:<7} {nimg:<7} {os.path.basename(zpath)}  [{ok}]")
