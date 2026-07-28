#!/usr/bin/env python3
"""Flip a DADS5250 lab-video recording status inside a Module HTML.

Usage:
  python3 mark_lab.py M03 2 done      # mark M03's 2nd lab video RECORDED
  python3 mark_lab.py M03 2 todo      # mark it back to NOT RECORDED
  python3 mark_lab.py status          # print the whole recording tracker

Lab videos are the SCREEN RECORDING / LAB WALKTHROUGH placeholders in
scripts/M0*_*/M0*_Module.html. The 24 scripted studio videos are already
recorded and are not tracked here.
"""
import re, glob, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def module_file(mod):
    hits = glob.glob(os.path.join(BASE, f"{mod}_*/{mod}_Module.html"))
    return hits[0] if hits else None

def lab_blocks(text):
    # each lab placeholder = a vp-badges div containing vp-badge-type-lab
    return list(re.finditer(
        r'<div class="vp-badges">(?:(?!</div>).)*?vp-badge-type-lab(?:(?!</div>).)*?</div>',
        text, flags=re.S))

def title_before(text, pos):
    h = re.findall(r'>([^<>]{3,70})</h[1-4]>', text[:pos])
    return h[-1].strip() if h else "?"

def show_status():
    for f in sorted(glob.glob(os.path.join(BASE, "M0[1-6]_*/M0[1-6]_Module.html"))):
        mod = os.path.basename(f).split("_")[0]
        t = open(f, encoding="utf-8").read()
        for i, m in enumerate(lab_blocks(t), 1):
            done = "vp-badge-status-done" in m.group(0)
            mark = "[x] RECORDED    " if done else "[ ] not recorded"
            print(f"  {mod} lab {i}  {mark}  {title_before(t, m.start())}")

def flip(mod, idx, state):
    f = module_file(mod)
    if not f:
        sys.exit(f"no Module HTML for {mod}")
    t = open(f, encoding="utf-8").read()
    blocks = lab_blocks(t)
    if not (1 <= idx <= len(blocks)):
        sys.exit(f"{mod} has {len(blocks)} lab videos; {idx} out of range")
    b = blocks[idx - 1]
    if state == "done":
        nb = b.group(0).replace("vp-badge-status-todo", "vp-badge-status-done").replace(">NOT RECORDED<", ">RECORDED<")
    else:
        nb = b.group(0).replace("vp-badge-status-done", "vp-badge-status-todo").replace(">RECORDED<", ">NOT RECORDED<")
    t = t[:b.start()] + nb + t[b.end():]
    open(f, "w", encoding="utf-8").write(t)
    print(f"{mod} lab {idx} -> {'RECORDED' if state=='done' else 'not recorded'}")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "status":
        show_status()
    elif len(sys.argv) == 4:
        flip(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print(__doc__)
