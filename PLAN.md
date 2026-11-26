# PLAN: excel-assessment-grading rebuild

Handover checklist. Anyone picking this up, human or AI, should be able to continue from here. Last updated 26 November 2026 (end of day 1).

## 1. What this project is

We're rebuilding the `excel-assessment-grading` Claude skill. It grades Opensignal Market Research Analyst candidates' Excel take-home exercise (Part A, Q1–Q6).

- **Goal** (Joni Factor, 17 Nov): let the scoring crew trust the skill enough to roll it out, cutting the number of reviewers and the time per review.
- **Scope decision (D1, Toby):** the new skill traces mistakes, as the original does, *and* acts as a first-pass grader that scores each question 1–3 and gives a Yes/No recommendation. The reviewer makes the final decision.
- **Stakeholders:**
  - Toby Young: owner of this rebuild
  - Gina Muan: AI team
  - Joni Factor: owns the hiring process and the exercise
  - Lisette Labbe: coordinates reviews
  - Jeremy White: built the original skill

## 2. Working rules (read before doing anything)

1. **Never commit or push without Toby's review.** Prepare changes and leave them uncommitted; Toby reviews and commits.
2. **Candidate data never goes into git.** The repo is pushed to a shared, private GitHub remote. Submissions (even anonymised), the ID-to-name mapping, original downloads and form exports are all git-ignored.
3. **Anonymise by replacing, never emptying.**
   - Identity fields become the submission ID (`sub-NNN`).
   - Candidate names in text become `[CANDIDATE]`.
   - Reviewers become `reviewer-NN`.
   - Gendered pronouns become "the candidate".
   - Dates are month-only.
   - Details: `notes/test-set-plan.md` §2a and §3.
4. **Scripts print counts only.** No one should need to open a candidate's sheet or see a name to anonymise it.
5. **Place names in the exercise data are not personal data.** They're exercise content; never alter them.
6. **Staff names in `notes/` are acceptable for now** (Toby, 26 Nov). They're not acceptable in `tests/` or the skill.

## 3. Where things are

| Path | What | In git? |
|---|---|---|
| `PLAN.md` | This file | Yes |
| `README.md` | Layout, data rules, how to anonymise and rebuild the test set | Yes |
| `excel-assessment-grading/` | **The new skill** (what ships). Still empty: `references/` and `scripts/` hold only `.gitkeep` | Yes |
| `resources/old-skill/excel-assessment-grading/` | Unmodified copy of the original skill, for reference | Yes |
| `resources/answer-key-2021-05-31.xlsx` | 2021 answer key ("DO NOT DISTRIBUTE"; ask Joni for a copy) | **No** |
| `templates/exercise-template-2026-08-24.xlsx` | Current candidate template (Drive link in README) | **No** |
| `tests/inputs/verdicts.csv` | Reviewer scores and anonymised comments for the 19 test submissions | Yes |
| `tests/inputs/submissions/` | Anonymised `sub-101` to `sub-120` (no `sub-104`) | **No** |
| `tests/scripts/` | `survey_xlsx.py`, `anonymise_xlsx.py`, `select_test_set.py`, `build_test_set.py` | Yes |
| `private/` | Originals, `manifest.tsv` (ID ↔ form row ↔ candidate), `excluded.tsv`, `reviewers.tsv`, `staff.txt`, form export, `selection.csv` | **No**, on Toby's machine only |
| `notes/excel-assessment-grading-review.md` | Toby's review of the original skill (the main reference) | Yes |
| `notes/knowledge-inventory.md` | Every item needed (K), decisions (D), conflicts (C) | Yes |
| `notes/open-questions.md` | Questions for Joni, Lisette, Jeremy and Allyson (Q1–Q24) | Yes |
| `notes/template-defects.md` | 9 defects in the candidate template, to report to Joni | Yes |
| `notes/test-set-plan.md` | Form statistics, sampling plan, anonymisation procedure, test set as built, file-route finding | Yes |
| `notes/archive/` | Slack extracts (stakeholder replies, #excelassessment channel history) | Yes |

**Someone without Toby's machine** won't have the git-ignored files. They need:

- the template, from the Drive link in the README;
- the 2021 key, from Joni;
- the test submissions and `private/`, from Toby (never via git).

## 4. Checklist

### Stage 0: Review and setup ✅

- [x] Review the original skill (`notes/excel-assessment-grading-review.md`)
- [x] Gather stakeholder input from Slack (`notes/archive/`)
- [x] Build the knowledge inventory, conflicts log and open questions
- [x] Download and compare the template and the 2021 key. Every number recomputes; nine template defects were found, including a **missing percent-change formula**
- [x] Read the scoring-form header: each question is scored 1–3, plus a Yes/No recommendation
- [x] Set up the repo layout, `.gitignore` and README; private GitHub remote `toby-young-os/excel-assessment-grading-skill`

### Stage 1: Test set ✅ (branch `test-set`)

- [x] Agree the sampling plan (unequal by group, max 2 per reviewer, about 6 held back)
- [x] Write and test the survey and anonymiser scripts (trial on 6 files, all PASS)
- [x] Select, download, anonymise and verify the test set: **19 submissions** (9 Yes / 10 No, 6 held back), covering every file route
- [x] Code the reviewers, replace pronouns, use month-only dates; full rescan of `tests/` clean
- [x] Copy the original skill to `resources/old-skill/`
- [ ] **Toby: push `test-set`** from his Mac (`git push -u origin test-set`). Pushing is blocked inside Cowork. Two commits are waiting: `23f04d5` and `564b6d3`
- [ ] Toby: review and merge `test-set` into `main`
- [ ] *Later, after consulting Jeremy and Joni:* add the 2 confirmed AI-use cases (K11, Q17) and Jeremy's 3 hand-graded assessments (K10, Q15)

### Stage 2: Rebuild brief (next)

- [ ] Create a branch (e.g. `brief`)
- [ ] Write `notes/brief.md`, one document:
  - your review as the structure;
  - the Slack material and the reference findings;
  - links to the conflicts (C1–C12) and decisions (D1–D6);
  - Joni's weighting of the competencies (`notes/archive/excel-assessment-slack-responses.md` §8);
  - the file-route requirement (C11)
- [ ] Reframe the review's gap 6: Q2 has no answer cells; check the Workbook 2 values (C9)
- [ ] Move `notes/excel-assessment-grading-review.md` to `notes/archive/` (decision D5)
- [ ] Toby reviews and commits

### Stage 3: Rebuild the skill

- [ ] Use the `skill-creator` skill; keep the name `excel-assessment-grading`
- [ ] `references/`:
  - a rebuilt `answer-key.md`, salvaging the old one's "wrong path" figures;
  - the exact exercise instructions as text, unless D2 decides to fetch them at run time
- [ ] `scripts/`:
  - verification rewritten from `verify_candidate.py`, hardened against the review's §3 list;
  - file-route detection (from `tests/scripts/build_test_set.py`);
  - dump script and shared helpers, with a proper XML parser
- [ ] Output that matches the scoring form: Q1–Q6 scores 1–3, comments, Yes/No, plus traced root causes, AI-use concern and a "not verified" section
- [ ] Decide D2 (fetch the instructions at run time, or build them in) and D6 (anonymise before grading)

### Stage 4: Evaluate

- [ ] Run the skill on the 13 working submissions; save reports to `tests/outputs/`
- [ ] Measure agreement for each group and each question, not overall
- [ ] Iterate, then a final check on the 6 held-back submissions

### Stage 5: Package and hand over

- [ ] Package `excel-assessment-grading.skill`; update the README
- [ ] Send `notes/template-defects.md` to Joni (Q19)
- [ ] Confirm the AI policy allows a skill that scores and recommends (Q1)

## 5. Waiting on people (see `notes/open-questions.md`)

| Who | What | Questions |
|---|---|---|
| Toby | Internal AI policy for applicant assessment | Q1 |
| Joni | Grading rulings: percent change (formula missing), Q6 "comparisons", Sprint-only cascade, no work shown, Excel vs Google Sheets, work placement | Q5–Q9, Q21, Q22 |
| Joni | Model answers for 3a, 4a, an updated 4b and 5a; what a score of 2 means; success measures; the 57% vs "30% pass" question | Q2, Q11, Q12, Q23 |
| Jeremy | His 4 screenshots and 3 hand-graded assessments | Q15 |
| Lisette / Nizar | Permission to use the AI-use cases; a shared folder of submissions; keeping original emailed files | Q9, Q14, Q17 |
| Joni | Use of the "Hired" tab; older form responses | Q13, Q20 |

**Monday sync (30 Nov):** a good chance to clear the grading rulings and get the missing materials. Jeremy is free from midday only.

## 6. Things that will trip you up

- **Pushing to GitHub is blocked in Cowork.** Commits work; push from a terminal on your own machine.
- **Many Slack "files" are Drive previews, not uploads.** `file_content_unavailable` means: use the Drive link in the same Slack message.
- **The Drive connector can't download files over 10 MB.** OneDrive links can't be downloaded at all.
- **Native Google Sheets** have to be exported as xlsx; they lose their pivots. Excel files that went through Google save charts as pictures. The skill must detect this and not penalise it (C11).
- **The scoring-form export contains candidate names and emails.** Only ever read it by column, or inside a script that prints counts.
- **Short names collide with exercise data** (e.g. a three-letter first name inside a city name). Use whole-word matching and ignore template text.

## 7. Prompt to resume in a new AI session

> I'm continuing the rebuild of the `excel-assessment-grading` Claude skill in this repository. Read `PLAN.md` first, then `README.md`, `notes/knowledge-inventory.md` and `notes/open-questions.md`. Follow the working rules in PLAN.md §2: in particular, never commit or push without my review, and never put candidate data in git. We're at Stage 2: write the rebuild brief (`notes/brief.md`). Ask me before making any decisions listed as open.
