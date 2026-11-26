# Test set plan: excel-assessment-grading rebuild

How the test set is chosen, anonymised and checked. Written 26 November 2026. Codes (K, C, Q) refer to `knowledge-inventory.md` and `open-questions.md`.

---

## 1. Source data: the scoring form responses (K7)

Read with counts only: no names, emails or comments were displayed. The export used for counting was kept only in a temporary sandbox folder, never in the project.

- **240 responses**, 13 Nov 2025 to 19 Nov 2026, from **20 reviewers**.
- **Recommendation:** 137 Yes (57%), 103 No. This doesn't fit Joni's "30% or less pass the assessment" (17 Nov); see Q23.
- **141 responses date from Jul–Nov 2026.** The current template (with the AI rule) was last modified on 24 Aug 2026.
- **Reviewers use half-points:** scores of 1.5 and 2.5 appear 14 times, although the form says "1 - no, 3 - perfect" (see Q12).
- **9 score cells contain text** (reviewer comments) instead of numbers, across 6 rows.
- **A "Hired" tab has 15 rows**, possibly real hiring outcomes. Not opened (see Q20).

**Total score vs recommendation.** The total is the sum of the six question scores (6–18). It's our own measure; reviewers don't calculate it. Six rows with text scores are excluded:

| Total | No | Yes | Reading |
|---|---|---|---|
| 6–8 | 31 | 2 | Clear fail |
| 9–11 | 32 | 1 | Clear fail |
| 12–14 | 26 | 27 | **Borderline: an even split** |
| 15–16 | 6 | 36 | Strong |
| 17 | 5 | 25 | Near-perfect |
| 18 | 1 | 42 | Perfect |
| **All** | 101 | 133 | |

**Per-question score counts** (1 / 2 / 3; half-points omitted):

| Question | 1 | 2 | 3 |
|---|---|---|---|
| Q1 | 74 | 45 | 121 |
| Q2 | 44 | 36 | 157 |
| Q3 | 52 | 34 | 150 |
| Q4 | 52 | 69 | 113 |
| Q5 | 62 | 71 | 100 |
| Q6 | 56 | 80 | 98 |

Q1 (filtering) has the most 1s. Q4 to Q6 have the most partial scores.

**Notable cases:**

- 12 candidates scored 15 or more but got a No. The likely reasons are suspected AI use or sloppy work.
- 3 candidates scored 11 or less but got a Yes.

---

## 2. Sampling plan (about 20 submissions)

The data is unbalanced, so sampling in proportion would give mostly near-perfect submissions and miss the cases that test judgement. Sample deliberately by group:

| Group | Count | Why |
|---|---|---|
| Clear fail (6–11, No) | 4 | Pick different root causes: Sprint-only cascade, wrong win share metric, no work shown |
| Borderline (12–14) | 6, split 3 Yes / 3 No | The hardest calls, where a first-pass grader adds most value |
| Strong (15–16, Yes) | 3 | Check the skill doesn't over-penalise small slips |
| Near-perfect (17–18, Yes) | 3 | Check it doesn't invent errors |
| High score but No | 2 | Probably AI suspicion or sloppiness; tests the parts beyond correct answers |
| Low score but Yes | 1 | A reviewer overrode the scores; useful edge case |
| Confirmed AI-use cases | 2 | The Aug 2026 and Dec 2025 threads (K11, Q17) |
| Jeremy's 3 hand-graded assessments | (overlap) | Slot them into whichever groups they fit (K10, Q15) |

**Rules for picking within each group:**

1. **Prefer submissions from after Aug 2026**, so they match the current template.
2. **No more than 2 per reviewer**, so no single reviewer's leniency or strictness skews the set.
3. **Cover every route a file can arrive by:** native Excel, Google Sheets export, and Excel file stored in Drive (see section 4).
4. **Keep about 6 of the 20 back** for a final check, so the skill isn't tuned to the very examples it's tested on.

**When reporting results**, measure agreement for each group and each question, not overall. Because 57% of verdicts are Yes, a skill that says Yes to everything would still look 57% accurate.

---

## 3. Anonymisation procedure

**Scripts** (in `tests/scripts/`):

- **`survey_xlsx.py`:** reports where personal data could sit in a submission. Counts only.
- **`anonymise_xlsx.py`:** replaces identity data and verifies the result. Counts only.

**Policy (option C, agreed 26 Nov):** replace identity data, never empty it. Several identity fields are also evidence of how the candidate worked (desktop Excel vs Google Sheets, pivots refreshed locally, OS and folder), so they must keep their shape.

| Location | Replaced with |
|---|---|
| Filename | `sub-NNN.xlsx` |
| `core.xml` `creator` and `lastModifiedBy` | `sub-NNN`. `creator` is replaced too, even when it is only the template author |
| `app.xml` `Company`, `Manager` | `sub-NNN` |
| Pivot cache `refreshedBy` | `sub-NNN` |
| Comment authors, threaded-comment persons (name and user ID) | `sub-NNN` |
| File path (`absPath`) | Only the username segment, e.g. `/Users/sub-NNN/Downloads/` |
| OneDrive/SharePoint personal URL segment | `sub-NNN` |
| Email addresses | `[EMAIL]` |
| Names in free text (cells, text boxes, chart titles, comments) | `[CANDIDATE]` |

**Safeguards:**

- **No re-saving.** The file's internal parts are edited directly and every other byte is copied unchanged. Re-saving through Excel or a spreadsheet library can drop charts, pivots and text boxes, which are the grading evidence.
- **Names come from several sources:** the Slack request message, the filename, the author fields, `refreshedBy` and comment authors. They're never printed.
- **Whole-word matching only.** Candidates' surnames can appear inside place names in the data. Two-letter names (e.g. a surname like "Fu") only match as part of the full name.
- **Text from the blank template is never altered**, and the template author's name is excluded from the name list.
- **Images are OCR-checked** for names and emails. Any hit is flagged for manual redaction.
- **Sheet names containing a name are flagged, not renamed**, because renaming would break formulas.
- **The ID-to-name mapping is kept outside the project folder.**

**Checks run on every output:**

1. Every internal part still parses, and the file opens.
2. No whole-word name hits remain, and no file-path usernames remain.
3. Worksheets, charts, pivot tables, pivot data, tables and text boxes are byte-identical to the original, unless a logged replacement touched them.
4. An independent re-survey of the output comes back clean.

### Trial on 6 varied submissions (26 Nov)

The samples were chosen to test the procedure; they are not the test set.

| ID | How it arrived | Where the name appeared | Result |
|---|---|---|---|
| sub-001 | Slack attachment | author fields, pivot `refreshedBy`, file path | PASS |
| sub-002 | Slack attachment, `.xlsb.xlsx` | author fields, 2 pivot caches, file path | PASS |
| sub-003 | Slack attachment, no name in filename | author fields, file path, **name typed in a cell (2)** | PASS |
| sub-004 | Slack attachment, initials only in filename | author fields, 6 pivot caches, file path | PASS |
| sub-005 | Google Sheets export (via Drive) | nowhere (Google strips the file properties) | PASS |
| sub-006 | Excel file stored in Drive | `creator` only; 4 images, which OCR showed contain no names | PASS |

**Lessons from the trial:**

- **Personal data is mostly in metadata.** Grading content had no names except sub-003, where the candidate typed their name into a cell.
- **The filename isn't a reliable name source.** Two of six filenames had no full name. The Slack request message and the file's metadata covered both.
- **Simple find-and-replace would corrupt the data.** Name fragments occur inside place names (9 partial hits in sub-006 alone); whole-word matching correctly left them alone.
- **No comments, hyperlinks, emails or cloud URLs were found** in any of the six.

---

## 4. Important: how a file arrives changes what can be graded

The same exercise looks very different inside the file depending on how it reached us:

| Route | Pivot tables | Pivot data | Charts | Author metadata |
|---|---|---|---|---|
| Native Excel (subs 001–004) | Present | Present | Readable chart objects | Present |
| Google Sheets export (sub-005) | **None** | None | Readable chart objects | Stripped |
| Excel file stored in Drive (sub-006) | Present | **Missing** | **Saved as pictures** (`Chart1.png`, etc.) | Partial |

**What this means for the skill:**

- For a Drive-stored file, the skill can't read chart series, so the Q2 and Q6 chart checks can't run. Its hidden-row pivot check also has no pivot data to work with.
- For a Google Sheets export, there are no pivots to inspect. "No pivot tables" may be how the file was exported, not proof that the candidate hardcoded values. Reviewers treat hardcoding as a red flag, so a wrong inference here would be unfair to the candidate.
- This is the same Excel-vs-Google-Sheets problem reviewers have reported (D3, OQ6).

**Requirements:**

- The rebuilt skill must detect the route from markers in the file.
- It must say which checks it couldn't run, and it must not penalise anything missing because of the export.
- The test set must include each route on purpose.
