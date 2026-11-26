# Knowledge inventory: excel-assessment-grading rebuild

Working file. Lists everything the rebuild needs, where it is, and who owns it. It feeds the single rebuild brief and the Monday sync agenda. Started 26 November 2026.

**Status key:** Have = readable now · Linked = location known, not yet pulled · Missing = location unknown or not yet provided · Decision = needs a team call, not a document

**Gap and question codes:** G1 to G9 are the gaps in `excel-assessment-grading-review.md` section 2. OQ1 to OQ6 are the open questions in `notes/archive/excelassessment-channel-extract.md` Part 4.

---

## 1. Inventory

### Exercise and answer materials

| # | Item | Status | Location | Owner | Covers | PII |
|---|---|---|---|---|---|---|
| K1 | Exercise template, all tabs (Welcome, Resources, Instructions (New), Answers (New), cma_lkup, Monthly Data, Workbook 1 to 6) | **Have** | `templates/exercise-template-2026-08-24.xlsx`, from [Google Drive](https://docs.google.com/spreadsheets/d/12blUDiUeMe8I7Bd33Tzxb0T3BQjKnpoX/edit?gid=684559432#gid=684559432) (last modified by Joni 24 Aug 2026). Instruction text is in text boxes, not cells | Joni | G1, G7, G8 · OQ1, OQ2, OQ5 | No |
| K2 | 2021 answer key workbook (`New Excel Exercise (Answer Key) - 05 31 2021 (11).xlsx`) | **Have** | `resources/answer-key-2021-05-31.xlsx` (from Slack file `F066XEAM62U`, pinned in #excelassessment ([message](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1700227496156819)); not found in Drive). Raw data identical to K1; all answers recompute correctly. Contains model answers (see K4) and Q2/Q6 reference charts | Joni | OQ4 · checks the skill's `answer-key.md` | No |
| K3 | Current skill (SKILL.md, answer-key.md, scripts) | Have | Installed copy in this session; [claude.ai skill link](https://claude.ai/customize/skills/id/plugin_01ERPJJXbMf5o1nmGbB5hTLk) | Jeremy | Salvage list (review §6) | No |
| K4 | Model answers for written questions 3a, 3b, 4a, 4b, 5a | **Partial** | K2 has one-line answers for 3b, 4b and 5a, plus Q6 commentary. Gaps: none for 3a or 4a; 4b answers the old "worse" wording; 5a doesn't cover extra data sets; Q6 commentary has the % direction wrong. Joni said "Pulling this now" (25 Nov) | Joni | G4 | No |
| K5 | Part B of the exercise | Probably dropped | The current template has no Part B tab. The 2021 key labels its tabs "Part A - …", so Part B likely existed once. Confirm | Joni | G8 | No |

### Scoring and calibration

| # | Item | Status | Location | Owner | Covers | PII |
|---|---|---|---|---|---|---|
| K6 | Current scoring form (questions and scale) | **Mostly have** (via the K7 header row): each of Q1–Q6 scored "1 - no, 3 - perfect" with a comment prompt (Q1 filter, Q2 win share chart, Q3 win share calculation, Q4 percent change calculation, Q5 and Q6 general); then a Yes/No on moving to a phone screen plus free comments. What a 2 means is not defined. The form itself wasn't found in Drive | [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSd5QQHrIgKPrviZmGeDkhH3uW5dLM2bTVTd3XPNmEQeXhmDXg/viewform) (shared form since Nov 2025) | Lisette | G2 · OQ3 | No |
| K7 | Scoring form responses (240 evaluations, "Form Responses 1") | Linked (confirmed accessible, view-only; only the header row read, under the privacy rule). Tabs: Form Responses 1 (24 cols × 341 rows), Pivot Table 2, **Hired** (possibly hiring outcomes; not opened) | [Excel Eval Form Template (Responses)](https://docs.google.com/spreadsheets/d/1am5Qh_fJK1nR0wHhAiWCmp94jPQhqYwKYY05Yv0s1Rs/edit?gid=1987702786#gid=1987702786) | Joni | G3, G5 | **Yes** |
| K8 | Older per-candidate form responses (2023 to about Oct 2025) | Missing | Separate response sheets, not located | Joni | G3 | **Yes** |
| K9 | Past submissions | Linked | Linked or attached in each #excelassessment request; no shared folder confirmed | Lisette | G3, G9 | **Yes** |
| K10 | Jeremy's 4 screenshots (output format and 3 hand-graded comparisons) | Missing | Forwarded into the group DM on 17 Nov; images can't be read | Jeremy | G3 · baseline for the current skill | Possibly |
| K11 | Confirmed or suspected AI-use submissions | Linked | [Aug 2026 thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1786453594888009), [Dec 2025 thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1765980543812219) | Lisette | G5 | **Yes** |

### Context and policy

| # | Item | Status | Location | Owner | Covers | PII |
|---|---|---|---|---|---|---|
| K12 | How reviewers weigh the competencies | Have | Joni, group DM 25 Nov (`notes/archive/excel-assessment-slack-responses.md` §8) | Joni | G2 | No |
| K13 | Project goal and success measure | Have (partly) | Joni, group DM 17 Nov: under 30% pass, aim for fewer reviewers and less time, and confidence to roll out to scorers | Joni | Scope | No |
| K14 | How often the exercise changes | Have | Group DM 24 Nov: questions unchanged for 10+ years, instructions slightly reworded since the 2021 key, no changes in at least a year | Joni, Jeremy, Lisette | G7 | No |
| K15 | Role context: seniority, time allowed | Missing | No time limit found in the K1 instruction text | Joni | G2 | No |
| K16 | AI policy for applicant assessment | Missing (Toby sourcing) | Cited by Jeremy (17 and 25 Nov). The K1 Instructions say "Do not use AI for this exercise" and link to the public [careers page](https://www.opensignal.com/about/opensignal-careers) for Opensignal's AI-in-hiring philosophy. The internal policy is still needed | Toby | Constraints on D1 | No |
| K17 | Reviewer training material (Allyson's demo, Aug 2026) | Missing | Training is done by pairing; no written guide found | Allyson | G3 | No |
| K19 | Template defects list | Have | `template-defects.md` (9 defects; to report to Joni) | Toby | G1, G7 | No |
| K20 | Form response statistics, sampling plan, anonymisation procedure and trial results | Have | `test-set-plan.md` | Toby | G3, G5, G9 | No |
| K22 | Test set (19 submissions) and verdicts | **Have** | `tests/inputs/verdicts.csv` (reviewers coded, pronouns replaced); anonymised files in `tests/inputs/submissions/` (git-ignored); built 26 Nov, all 19 PASS. The one "low score but Yes" case was removed as an outlier (score-entry error) (`test-set-plan.md` §2a). AI-use cases (K11) and Jeremy's three (K10) to be added after consulting Jeremy and Joni | Toby | G3, G9 | Submissions: anonymised |
| K21 | Survey and anonymisation scripts | Have | `tests/scripts/survey_xlsx.py`, `tests/scripts/anonymise_xlsx.py` (tested on 6 submissions, all PASS) | Toby | G9 | No |
| K18 | Gina's request sheet (AI Training Workshop Requests) | Linked | [Google Sheet](https://docs.google.com/spreadsheets/d/1dh7KH5LvTy7oXUUmx0VFAPd24eeI6nwLpR_0X247RbM/edit?gid=458942398#gid=458942398) | Gina | Scope (low priority) | No |

### Decisions (not documents)

| # | Decision | Depends on | Who decides |
|---|---|---|---|
| D1 | **Decided (Toby, 26 Nov):** the new skill traces mistakes as now *and* acts as a first-pass grader that scores and recommends. The AI policy (K16) may still constrain how this is worded or rolled out | — | Done |
| D2 | Fetch instructions at run time (step 0) or bundle them in the skill? **Deferred** until the skill is written | K1, K14 | Toby |
| D6 | **Design option (Toby's idea, 26 Nov; assessed as viable): anonymise before grading.** The skill downloads the submission, runs `anonymise_xlsx.py` as step 0, grades only the anonymised `sub-NNN` copy, and returns results under the ID, never reading the candidate's name. **Why it works:** the trial showed grading content stays byte-identical, and replacing identity fields (not emptying them) keeps the file-origin evidence. **Adjustments:** (1) return results under the ID (a block to paste into the scoring form, or a separate results sheet) rather than writing into the candidate's sheet, which reviewers can only view and which would alter the evidence; the reviewer links the result back to the candidate. (2) Claim it *minimises* exposure: the name still arrives in the filename, Slack message or Drive title before the script runs, so the design must make sure Claude never opens the original or repeats the name. **If adopted,** a slimmed-down anonymiser becomes part of the skill | Q1 (AI policy), Q24 | Toby, Joni, policy owner |
| D5 | **Decided (Toby, 26 Nov):** once the brief is written, `excel-assessment-grading-review.md` moves to `notes/archive/` unchanged, alongside the two Slack files | — | Done |
| D3 | Which version counts when Excel and Google Sheets differ? | OQ6 | Joni, Lisette |
| D4 | Is Part B in scope? | K5 | Joni |

---

## 2. Privacy rule for downloads (point 4)

- **Download now** (no candidate data): K1, K2, K3, K4, K5, K6 (form questions only), K16, K17, K18.
- **Do not download in bulk:** K7, K8, K9, K11. Pull these only when choosing the test set, one file at a time, and anonymise as they come in:
  - Rename files to a neutral ID (e.g. `sub-001.xlsx`) and keep the ID-to-thread map outside the repo.
  - **Replace, never empty (option C, decided 26 Nov):** identity fields, including `creator`, become the submission ID. Names in free text become `[CANDIDATE]`. Full procedure in `test-set-plan.md` §3, run with `tests/scripts/anonymise_xlsx.py`.
  - From K7, keep only the verdict, scores and reviewer comments, plus a submission ID. Reviewer comments may name the candidate, so apply the same name replacement.
  - Neither Claude nor Toby views sheet contents: scripts print counts only.
- Reviewer names (Opensignal staff) stay, since they matter for calibration.
- Downloads go to `templates/` (exercise template) and `resources/` (other source material). Anonymised submissions go to `tests/inputs/submissions/` (git-ignored).

---

## 3. Conflicts log (point 5)

Recorded, not resolved. When sources disagree, the review file outranks the Slack responses, which outrank the channel extract. These are still flagged here for the team to decide.

| # | Conflict | Source A | Source B | Needed to resolve |
|---|---|---|---|---|
| C1 | **Resolved by D1 (trace and score).** Was: **Tracer or scorer.** The skill was built never to score and "only ever work in the candidate's favor". The goal is now rollout to scorers with fewer reviewers | Jeremy, 17 and 25 Nov; current SKILL.md | Joni, 17 Nov; Gina's question, 25 Nov | D1, K16 |
| C2 | **Percent change.** Heavily penalised (some reviewers treat it as an automatic No), but one reviewer gave full marks for simple difference because the Resources-tab formula didn't display. **Confirmed 26 Nov:** the equation is missing from the current template, so candidates never see the formula (`template-defects.md` D-1) | Joni, 25 Nov | Ethan MacRae, Jul 2025; K1 | Joni's ruling on grading until the template is fixed |
| C3 | **Q6 needs two or more comparisons.** Treated as an instruction that's docked when missed, but reviewers say the wording is unclear, and every early submission gave one chart. **Confirmed 26 Nov:** wording unchanged since 2021 ("graphically show some comparisons") | Joni, 25 Nov; Allyson's demo | Jeremy and Allyson, Aug 2026; K1 | Joni's ruling (D-6) |
| C4 | **Resolved 26 Nov.** Was: **answer-key currency.** The raw data is identical and every number in K2 and the skill's answer key recomputes from K1. Exceptions: the K2 4b model answer (old "worse" wording) and the K2 Q6 commentary (direction wrong). The skill's answer-key.md already corrects both | Review §3; Jeremy, 24 Nov | K1, K2, K3 comparison | Done |
| C5 | **Partly resolved 26 Nov.** Was: **the Sprint-only filter trap.** The comma after "Sprint Wireless" that Jay suggested has since been added to K1, so the wording was softened, not kept as a deliberate trap. Still open: how to grade candidates who make the mistake anyway | Joni, 25 Nov | Jay Frongillo, Aug 2025; K1 | Grading ruling only |
| C6 | **Questions change often vs rarely.** Gina's working assumption was a semi-monthly cycle and a general-purpose grader. Stakeholders say the questions rarely change | Gina, 24 Nov | Joni, Jeremy, Lisette, 24 Nov | Settled by K14 (rarely); affects D2 only |
| C7 | **A correct answer with no work shown.** Some reviewers give 3 plus a flag, while a missing workbook can be read as a single slip. Joni treats hardcoded values as a consistent red flag. The scale is now known (1–3 per question), but what a 2 means is not | Allyson, Nizar, Aug 2026 | Joni, 25 Nov | Joni's ruling |
| C8 | **The Q6 reference figure in the 2021 key is wrong.** The K2 commentary says NY is "15.2% lower" than overall. In fact NY is 13.2% below overall (overall is 15.2% above NY). Reviewers grading against K2 may mark correct captions wrong | K2 | K3 answer-key.md; recomputed 26 Nov | Tell reviewers; the skill uses the corrected figure |
| C9 | **Review gap 6 ("Q2 not checked through the answer cells") is misframed.** Q2 has no answer cells: the answer is a line chart on the Answers tab. The real check is the chart series plus the Workbook 2 pivot or formula values | Review §2 gap 6, §4 item 5 | K1, K2 Answers tab | Reframe in the brief |
| C11 | **Important: how a file arrives changes what's in it.** A Google Sheets export has no pivot tables. An Excel file stored in Drive has no pivot data and saves charts as pictures. The skill could wrongly read missing pivots as hardcoding, and can't check chart series on Drive files. Reviewers see the same problem | Trial, 26 Nov (`test-set-plan.md` §4) | Review §3 (assumes native Excel) | The skill must detect the route and report checks it couldn't run; D3 decides which version counts |
| C12 | **Pass rate.** Joni says "30% or less pass", but 57% of form recommendations are Yes | Joni, 17 Nov | K7 counts (137/240) | Q23 |
| C10 | **Where Q2 and Q4 work belongs.** For Q2, the Instructions say Workbook 2 and the Answers tab says Workbook 1. For Q4, the Instructions no longer name Workbook 4 but the Answers tab does. Reviewers mark down missing work | K1 Instructions | K1 Answers tab | Joni's ruling. Suggestion: don't penalise placement until the template is fixed (D-4, D-5) |
