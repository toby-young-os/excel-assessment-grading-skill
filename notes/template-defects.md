# Excel exercise template: defects to report

For Joni, who owns the template. Found while comparing the current candidate template with the 2021 answer key on 26 November 2026. Not yet reported; Toby to send.

**Files compared**

- **Current template:** `Opensignal Exercise - Excel Exercise - NEW.xlsx` ([Drive](https://docs.google.com/spreadsheets/d/12blUDiUeMe8I7Bd33Tzxb0T3BQjKnpoX/edit), last modified by Joni on 24 Aug 2026). Local copy: `templates/exercise-template-2026-08-24.xlsx`.
- **2021 answer key:** `New Excel Exercise (Answer Key) - 05 31 2021.xlsx` (pinned in #excelassessment). Local copy: `resources/answer-key-2021-05-31.xlsx`.

The raw data in both files is identical, and every expected answer recomputes correctly from the template. The defects below are in the candidate-facing text only.

---

## High priority

### D-1. The formulas on the Resources tab are missing

The 2021 key shows both definitions as equations. In the current template the equations have been removed, so candidates see unfinished sentences:

| Definition | 2021 key shows | Current template shows |
|---|---|---|
| Win share example | "would be 25% = (100 × 25/100)" | "would be 25% = (100*)." |
| Percent change example | "the percent change is +10.1% = (28.3% − 25.7%) / 25.7%" | "the percent change is ." |

- **Likely cause:** the template was converted through Google Sheets, which drops Office equation objects.
- **Why it matters:** reviewers heavily penalise confusing percent change with a percentage-point difference, and some treat it as an automatic No. Yet candidates are never shown the formula they are judged against. Ethan MacRae reported this in #excelassessment in [Jul 2025](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1753476803429549), and it has not been fixed.
- **Suggested fix:** replace the equations with plain text that survives Google Sheets, for example "Percent change = (new − old) / old. E.g. (28.3% − 25.7%) / 25.7% = +10.1%." Then check the file in both Excel and Google Sheets.

## Medium priority

### D-2. The instructions name a tab that no longer exists

The Instructions tab says to put answers in the "'Part A - Answers' tab", and again in the "'Part - A Answers' tab". The tab is now called **Answers (New)**. Candidates who follow the text literally may look for the wrong tab.

**Suggested fix:** change both references to "Answers (New)", or rename the tab to match.

### D-3. Wrong question count

The Exercise text says "please answer the following 5 questions", but there are 6.

**Suggested fix:** change it to "6 questions".

### D-4. Q2 points to two different workbooks

The Instructions tab says "Please show work in 'Workbook 2'". The Answers tab says "Please show work on 'Workbook 1'". The 2021 key has the same inconsistency.

**Suggested fix:** use "Workbook 2" in both places.

### D-5. Q4 workbook instruction is inconsistent

The 2021 wording of Q4 ended "Please show your work in 'Workbook 4'". The current Instructions tab dropped that sentence, but the Answers tab still says "show work on 'Workbook 4'". Reviewers mark down missing work, so candidates should be told consistently where it goes.

**Suggested fix:** restore "Please show your work in 'Workbook 4'" to Q4 on the Instructions tab.

### D-6. Q6 wording is unclear on how many comparisons are expected

The text reads "graphically show some comparisons". Reviewers expect two or more and dock a point for one chart, but agree the wording is unclear ([Aug 2026](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1787163750599169)).

**Suggested fix:** if two or more is the requirement, say so, for example "show at least two comparisons (charts)".

## Low priority

### D-7. Welcome tab mentions "three exercises"

The Welcome tab says "Please use this data to complete the following three exercises". The workbook now contains one exercise (Part A, Q1–Q6).

**Suggested fix:** change it to "the following exercise".

### D-8. Leftover "Part A" labels

The Resources tab heading reads "PART A" and the Answers tab heading reads "PART A)", but there is no Part B.

**Suggested fix:** remove the labels, or keep them consistently if a Part B is planned.

### D-9. Typo on the Answers tab

The Q4 heading reads "Top 5 Underperforming Sprint Markets in **Notheast**".

**Suggested fix:** correct to "Northeast".

---

## Already fixed since 2021 (for reference)

- A comma was added after "Sprint Wireless" in the client sentence. This was suggested by Jay Frongillo in Aug 2025 to reduce the Sprint-only filter mistake.
- Question 4b now asks why a market performed **better** in August, which matches the data. In 2021 it asked about **worse**.
- A no-AI rule was added to the Instructions tab, with a link to the [careers page](https://www.opensignal.com/about/opensignal-careers).
- The "weekly and monthly" time-unit text was corrected to "monthly".
