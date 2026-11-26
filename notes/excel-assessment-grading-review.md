# excel-assessment-grading: review and rebuild plan

Reference notes and handoff for rebuilding the `excel-assessment-grading` Claude skill. Written 25 November 2026.

**Installed location:** `/mnt/skills/plugins/excel-assessment-grading/`

**Decision:** rebuild the skill from scratch once the materials below are gathered. Keep the skill name `excel-assessment-grading` so the new version installs as an update, not a duplicate.

---

## 1. What the skill does today

Opensignal uses a six-question Excel take-home (Part A, Q1 to Q6) to screen market research analyst applicants. The skill grades a candidate's completed workbook against an answer key and flags possible AI use. It triggers when someone uploads a submission (often named like `Opensignal Exercise - Excel Exercise - Candidate Name.xlsx`) or asks to check, grade or review one.

It assesses four competencies: Excel proficiency, attention to detail, instruction following, and conceptual understanding (win share, percent change). The reviewer makes the final decision; the skill gives no score and no hire recommendation.

### Contents

1. **`SKILL.md`**: grading workflow, rules for what is and is not an error, guidance on weighing patterns against one-off slips, written-answer and Q6 checks, AI-use guidance, and a fixed report format.
2. **`references/answer-key.md`**: exercise setup and client scope, expected answers for Q1 to Q6, reference numbers for common wrong paths, and the expected workbook layout (2021 template).
3. **`scripts/verify_candidate.py`**: recomputes expected answers from the candidate's own raw data and compares them with the answer tables, pivot sources, hidden-row filters, chart series and formulas. Also reports file origin and formula-complexity signals.
4. **`scripts/dump_candidate.py`**: writes every cell, formula, text box, chart, pivot setting and table to `dump.txt` for manual reading.
5. **`scripts/_common.py`**: shared helpers (regex-based XML parsing of the .xlsx zip, pivot source mapping, chart range resolution).

### Report format

Chat only: bottom line, Q1 to Q6 scorecard, patterns and root cause, red flags, written answers, AI-use concern level (none / low / medium / high), and a "not verified" section.

### Exercise questions (inferred, not verbatim)

The skill does **not** contain the question text. Reconstructed from the answer key:

| Q | Task (inferred) | Written parts |
|---|---|---|
| 1 | Filter the monthly data to the client scope (Sprint client; Northeast and Midwest regions; CMA population over 500,000), append Region, SubRegion and Population, place the result on Workbook 1 | |
| 2 | Sprint's monthly win share for 2014 on the filtered data | |
| 3 | Five Northeast CMAs with the lowest Sprint win share in August 2014 | 3a: steps taken; 3b: factors behind underperformance |
| 4 | July to August % change for those five markets | 4a: steps taken; 4b: why Sprint did better in August |
| 5 | Best performing Midwest SubRegion in 3Q14, with 2Q14 share and % change | 5a: why it succeeded; what extra data to use |
| 6 | Compare Sprint's win share in the New York, NY CMA to the overall win share from Q1 (charts, optional commentary) | |

Only Q6 is a near-quote. The skill covers Part A only, which suggests a Part B exists.

---

## 2. Gaps in the current skill

1. **Candidate-facing materials missing.** No verbatim questions, Instructions tab (including the no-AI rule) or Resources tab definitions. Instruction following is graded against a paraphrase.
2. **No role or hiring-bar context.** Seniority, time allowed, and how the competencies are weighed are absent, so severity calibration is guesswork.
3. **No calibration examples.** No graded sample submissions or model reports; tone and severity rest on prose rules alone.
4. **Thin written-answer rubric.** Only a "logical and directionally plausible" bar; no model or weak example answers.
5. **No AI-use baseline.** Signals are heuristics with no reference set of known human or AI-assisted submissions.
6. **Q2 not checked directly.** `verify_candidate.py` checks Q2 only through chart series, not the answer cells.
7. **Fragile to template variants** (details in section 3).
8. **Part B unaddressed.** Neither graded nor declared out of scope.
9. **No test set.** No fixtures to regression-test scripts or reports after changes.

---

## 3. Hardening needed (observed in the scripts)

- **Hard-coded sheet names:** `Monthly Data`, `cma_lkup`, `Workbook 1`. A renamed tab breaks the run or silently skips checks.
- **Positional column assumptions:** `Monthly Data` read as `usecols="A:E"`; `cma_lkup` columns renamed by position. Reordered or extra columns corrupt the recomputation.
- **Answer tables located by header text** (`market (cma)`, `subregion`) and assumed to start in column B. Edited headers or shifted layouts fail.
- **Q2 answer cells not compared** (see gap 6).
- **Fixed scan windows:** Google Sheets markers checked only in the first 400 rows (verify) or 3,000 rows (dump) of each tab.
- **Regex XML parsing** of workbook, pivot and chart XML rather than a proper parser; brittle against namespace or attribute-order differences.
- **Hidden-row detection assumes the header is row 1.**
- **NY CMA matched by `startswith("New York, NY")`**: fine for this data, but implicit.
- **Environment paths:** `SKILL.md` refers to `/sessions/*/mnt/uploads/` and `${CLAUDE_SKILL_DIR}`, which do not match claude.ai (`/mnt/user-data/uploads`). Paths should be environment-agnostic.
- **No explicit handling** for .xlsm, .xls, Google Sheets links or CSV submissions, and no clear failure message when the template is unrecognised.

---

## 4. Priorities (maximum robustness gain)

1. **Build a test set first.** Anonymized submissions with known outcomes, used to measure every change.
2. **Harden the scripts against template variants** (section 3). Prevents confident reports built on misread data.
3. **Add the candidate-facing materials.** Low effort, removes guesswork from instruction-following judgements.
4. **Add calibration examples.** Two or three graded submissions with reviewer verdicts; can reuse test-set files.
5. **Add the Q2 answer check.** Small, contained fix; do alongside item 2.

Items 2 and 5 are engineering work that can start immediately. Items 1, 3 and 4 depend on the hiring team, so request materials early.

---

## 5. Materials to gather

1. Blank copy of the exercise workbook, all tabs (Welcome, Resources, Instructions, Answers, data tabs, Workbook 1 to 6), plus Part B if it exists.
2. Five to ten anonymized past submissions across the quality range, each with the reviewer's verdict.
3. Any confirmed or strongly suspected AI-assisted submissions.
4. Role context: seniority, time allowed, how reviewers weigh the four competencies.
5. Model answers for the written questions (3a, 3b, 4a, 4b, 5a), if available.
6. Any template versions other than 2021 still in circulation.

---

## 6. Worth salvaging

- **Answer key numbers** (`references/answer-key.md`), especially the "wrong path" reference values (nationwide scope, region-only, SubRegion-instead-of-CMA, averaged quarterly shares, percent change as ratio, alternative Q6 baselines). The most valuable diagnostic content in the skill.
- **Recompute from the candidate's own raw data** rather than only comparing to fixed numbers; catches altered or mis-pasted data.
- **Hidden-row pivot check**: pivots built on an AutoFiltered sheet can include hidden rows; comparing pivot output with recomputed scopes shows which scope was used.
- **Percent-change-as-ratio detection** and the **flat near 20% series** check (numerator or denominator not carrier-specific).
- **Chart series matching** against known reference series.
- **Grading principles** in `SKILL.md`: trace each miss to its first wrong step, separate root causes from cascades, weigh patterns over single slips, never state unverified findings, keep a "not verified" section, flag (never decide) AI use.

---

## 7. Rebuild approach

- Use the `skill-creator` skill: capture intent, draft, run against test submissions, review, iterate, package.
- **Environment:** in Claude.ai, test runs are sequential, quantitative benchmarking is skipped, and trigger-description tuning needs Claude Code. With a real test set, **Cowork or Claude Code** is the better place for the rebuild.
- Start with the blank workbook: the verbatim questions shape the answer key, the rubric and the scripts.

---

## 8. Prompt for a new session

> I'm rebuilding the `excel-assessment-grading` Claude skill (installed at `/mnt/skills/plugins/excel-assessment-grading/`), which grades Opensignal candidates' Excel take-home exercises. The attached markdown file contains a review of the current skill, gaps, hardening needs, priorities, materials to gather and what to salvage. Read it and the current skill files, then use the `skill-creator` skill to help me rebuild it from scratch using the materials I provide. Keep the name `excel-assessment-grading`.
