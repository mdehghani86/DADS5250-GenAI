# DADS 5250 — Folder Map (reorganized 2026-09-23)

## Tree
- `1_Course_Material/`
  - `1_Presentations/` — lecture decks built by the module-deck system
    (`M03_Presentation/`, `M04_Presentation/`: build_deck.py + assets + pptx + pdf)
  - `2_Canvas_Pages/` — standalone HTML pages embedded in Canvas
- `2_Course_Evaluation/`
  - `1_Exams/` · `2_Projects/` — exams, rubrics, projects
- `9_Archive/` — junk and finished raw material. Moved here, never deleted
  (5S rule): duplicates report, stray pngs/xlsx/pdf, ME2350 sample, Studio Photos.
- Latest lecture PDFs also sit at the ROOT for grab and go.

## PROTECTED NAMES — do not rename these folders
`labs/ images/ quizzes/ scripts/ videos/ utils/ tools/ planning/` plus root
`CourseHome.html` and `index.html`. They are load bearing:
- Lab notebooks embed raw.githubusercontent.com URLs under `labs/...` and
  Colab badges pointing at these literal repo paths.
- Module pages in `scripts/` cross link `../../images`, `../../quizzes`,
  `../../planning/course-outline.html`.
Renaming any of them breaks distributed notebooks and published pages.

## Decision record
- 2026-09-23 · Decision: reorganize to numbered folders. Challenge raised:
  renaming git linked dirs breaks Colab badges, raw image URLs, and page
  cross links. MD's call: HYBRID reorg (numbered folders for everything not
  link bearing; protected names stay). Success = no broken notebook/page
  links; junk archived. Outcome: done, links verified untouched.
