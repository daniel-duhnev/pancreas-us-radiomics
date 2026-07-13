# Thesis Defense Prep — Study Hub

Study materials to teach yourself your own thesis from first principles and defend it
confidently. Everything here is grounded in your actual thesis (`thesis/*.tex`), your
committed results (`analysis/reports/*`), and the code audit (`docs/CODE_AUDIT_FINDINGS.md`).
No invented numbers or citations. General background (biology, physics, ML theory) is marked
as such and kept standard.

**Defense:** Thursday 16 July 2026, 09:00–10:00, room 55.309 (UPF).
**Committee:** Gemma Piella (supervisor), Miguel Ángel González Ballester, Sotiris Papadiamantis.
**Format:** 20–25 min presentation, then 15–20 min of questions *from each* committee member,
then you leave, they deliberate, and the grade is announced.

---

## The one thing to internalise

Your thesis is a **negative result protected by a positive control**. Radiomics texture from
grayscale ultrasound does **not** predict pancreas transplant rejection — but the *same statistical
analysis*, run on the clinical ARFI/DCE-US measurements, reproduces the published Bassaganyas et al.
(2025) result to three decimal places. That control validates your **statistical analysis and data
handling** (and proves it's powered to detect a real effect) — it turns "my model didn't work" into
"I proved the signal isn't there in B-mode texture." Note the scope: the clinical measurements are
tabular and never pass through your segmentation/PyRadiomics pipeline, so the control does **not**
validate the image-processing stage — that is defended separately (see M6). Everything else in your
defense hangs off this.

---

## How to use these materials

Each module has three layers you should hit in order:

1. **Read the guide** (`0X_*.md`) — first-principles explanation tied to your thesis.
2. **Drill the flashcards** (`flashcards.md`, that module's section) — rapid recall.
3. **Take the quiz** (`quizzes.md`) and check yourself against `quiz_answers.md`.

Then, when you've covered the modules, ask me to run a **mock defense** (see below).

### Suggested 5-day schedule

| Day | Modules | Goal |
|-----|---------|------|
| 1 | M0 Big picture · M1 Clinical background | Know the story + the clinical "why". |
| 2 | M2 Radiomics & pipeline | Explain every preprocessing/extraction choice. |
| 3 | M3 ML & statistics · M4 Results | Methodology fluency + numbers cold. |
| 4 | M5 Narrative · re-drill M4 | Tie it together; recall all key figures. |
| 5 | M6 Tough questions · M7 Logistics · mock defense | Defend under pressure. |

Adjust to the time you have. If you only have 2–3 days: M0 → `numbers_to_know.md` → M5 → M6,
then a mock defense.

---

## Files

| File | What it is |
|------|-----------|
| `00_big_picture.md` | 60-second pitch, the five objectives, the shape of the result. |
| `01_clinical_background.md` | Transplant, rejection, biopsy, B-mode/ARFI/DCE-US physics. |
| `02_radiomics_and_pipeline.md` | Preprocessing pipeline + PyRadiomics config + feature classes. |
| `03_ml_and_statistics.md` | Dataset structure, independent set, tests, ML pipeline, CV. |
| `04_results.md` | Every result explained, in order. |
| `05_narrative.md` | The physical explanation + between/within-patient insight + why it matters. |
| `06_tough_questions.md` | Anticipated hard questions with model answers (start here if short on time). |
| `07_logistics.md` | Defense format, committee, what to send, the flow on the day. |
| `numbers_to_know.md` | One-page cheat sheet of every figure to recall cold. |
| `flashcards.md` | Q→A decks per module, tagged Easy/Medium/Hard. |
| `quizzes.md` | Practice quizzes per module (questions only). |
| `quiz_answers.md` | Answer keys with explanations. |

---

## Mock defense — how to run it

When you're ready, tell me: **"Run a mock defense"** (optionally name a mode).

Modes:
- **"warm-up"** — gentle: definitions and "walk me through X". Builds fluency.
- **"standard"** — realistic mix: methods, results, interpretation.
- **"grill me"** — committee-level pressure using `06_tough_questions.md` (leakage, validity,
  provenance, "so what").
- **"rapid fire"** — many short questions, fast, to test recall.

How it works: I ask one question at a time as a named committee member. You answer *in your own
words* (type as if speaking). I then grade the answer (what was strong, what was missing or
imprecise), give a tighter model answer, and move on. At the end I summarise your weak spots so
you know what to re-drill.

Tip: answer out loud first, then type — the goal is spoken fluency, not written perfection.
