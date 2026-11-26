# Open questions: excel-assessment-grading rebuild

For Toby to review. Nothing here has been posted to Slack. Codes (K, C, D, OQ) refer to `knowledge-inventory.md`, and D-1 to D-9 refer to `template-defects.md`. Last updated 26 November 2026, after comparing the template, the 2021 key and the skill.

**Status:** Open · Toby sourcing · Toby to send · Deferred

---

## 1. Scope and context

| # | Question | Ask | Status | Ref |
|---|---|---|---|---|
| Q1 | Get a copy of the internal AI policy for applicant assessment. The template's instructions already say "Do not use AI for this exercise" and link to the public [careers page](https://www.opensignal.com/about/opensignal-careers). Does the policy limit a skill that scores and recommends? | — | Toby sourcing | K16, D1 |
| Q2 | What does success look like in numbers? For example, a target time per review, a number of reviewers, or a required level of agreement with human verdicts | Joni | Open | K13 |
| Q3 | Is Part B out of scope? The current template has no Part B tab, though "PART A" labels and "three exercises" remain (D-7, D-8) | Joni | Open (likely out of scope) | K5, D4 |
| Q4 | What seniority is the role, and how long do candidates get for the exercise? No time limit appears in the template instructions | Joni | Open (probably irrelevant) | K15 |
| Q19 | Report the template defects in `template-defects.md` to Joni so they can be fixed. D-1 (missing percent-change formula) is the priority | Joni | Toby to send | K19 |
| Q23 | Joni said "30% or less pass the assessment", but 57% of the 240 form recommendations are Yes. Does 30% refer to the whole hiring process, an earlier period, or something else? It affects what pass rate the skill should be calibrated to | Joni | Open | C12 |
| Q20 | Can the "Hired" tab (15 rows) in the form responses sheet be used? It may link verdicts to real hiring outcomes, which would make a strong test set. It contains candidate data, so it hasn't been opened | Joni | Open | K7 |

## 2. Grading rulings

| # | Question | Ask | Status | Ref |
|---|---|---|---|---|
| Q5 | **Not fixed (confirmed):** the percent-change formula is missing from the current template (D-1). Until it's fixed, should the skill accept a percentage-point difference, or penalise it as reviewers do now? | Joni | Open | C2 |
| Q6 | **Wording confirmed unchanged:** "graphically show some comparisons". Are two or more comparisons a firm requirement? | Joni | Open | C3, D-6 |
| Q7 | **The wording was softened:** a comma now follows "Sprint Wireless". How should the skill grade candidates who still filter to Sprint only, docking Q1 only or letting it cascade? Joni's 25 Nov summary describes the current practice; confirm it | Joni | Open (narrowed) | C5 |
| Q8 | How should the skill treat a correct answer with no work shown, in one workbook or in all of them? | Joni | Open | C7 |
| Q9 | When Excel and Google Sheets show a submission differently, which version counts? **Now more pressing:** the trial showed Google exports lose pivots and Drive-stored files turn charts into pictures (C11). Can Lisette keep the candidate's original emailed file for every submission? | Joni, Lisette | Open | D3, OQ6, C11 |
| Q21 | Should placement of Q2 and Q4 work be penalised while the template gives conflicting workbook instructions? | Joni | Open | C10, D-4, D-5 |
| Q22 | Reviewers who grade against the 2021 key's Q6 commentary may mark correct captions wrong ("15.2% lower" has the wrong direction). Should reviewers be told? | Joni | Open | C8 |

## 3. Materials to get

| # | Question | Ask | Status | Ref |
|---|---|---|---|---|
| Q11 | **Partly answered:** the 2021 key has one-line model answers for 3b, 4b, 5a and Q6. Still needed: answers for 3a and 4a, an updated 4b (the question now asks "better", not "worse"), and the 5a data-set part. Joni said "Pulling this now" on 25 Nov | Joni | Open (narrowed) | K4 |
| Q12 | **Mostly answered:** each question is scored 1 to 3 (1 = no, 3 = perfect), plus a Yes/No recommendation. What does a 2 mean? Is there any written guidance for reviewers on the scale? Reviewers also give half-points (1.5, 2.5; 14 times), so should the skill score in halves too? | Joni, Lisette | Open (narrowed) | K6, C7 |
| Q13 | Where are the older form responses from 2023 to about Oct 2025? | Joni | Open | K8 |
| Q14 | Is there a shared folder of past submissions, or do we take them one at a time from the channel? | Lisette | Open | K9 |
| Q15 | Can Jeremy share his 4 screenshots and the 3 hand-graded assessments he compared with the skill? | Jeremy | Open | K10 |
| Q16 | Was Allyson's grading demo (Aug 2026) recorded, or is there any written training guide? | Allyson | Open | K17 |
| Q17 | Can the two flagged AI-use cases (Aug 2026, Dec 2025) be used, anonymised, for calibration? | Lisette, Nizar | Open | K11 |

## 4. Deferred

| # | Question | Status | Ref |
|---|---|---|---|
| Q18 | Should the skill fetch the candidate instructions when it runs, or have them built in? | Deferred until the skill is written | D2 |
| Q24 | Adopt the "anonymise before grading" design (D6)? Depends on whether the AI policy (Q1) requires it, and on where reviewers want the results: pasted into the scoring form, or a separate results sheet | Deferred until Q1 is answered and the skill is written | D6 |

---

## Resolved

| Question | Answer | Date |
|---|---|---|
| Tracer or scorer? | Both: trace mistakes as now, and act as a first-pass grader that scores and recommends | 26 Nov (Toby) |
| Archive the review file? | Yes, once the brief is written | 26 Nov (Toby) |
| Post questions in Slack? | No. Open questions go in this file | 26 Nov (Toby) |
| Can Drive and Slack files be downloaded? | Yes. The template came from Drive and the answer key from Slack, both saved to `templates/` and `resources/` | 26 Nov |
| Q10: Does the 2021 key still match the template? | Yes for every number: the raw data is identical and all answers recompute. Exceptions: the 4b model answer (old wording) and the Q6 commentary (direction wrong), both already corrected in the skill | 26 Nov (comparison) |
| Was the Sprint-only wording changed? | Yes, a comma was added after "Sprint Wireless". Grading of the mistake is still open (Q7) | 26 Nov (comparison) |
| How should identity data be anonymised? | Replace with the submission ID (option C), including `creator`; never empty. Procedure tested on 6 submissions, all PASS (`test-set-plan.md`) | 26 Nov (Toby) |
| Was the percent-change formula fixed? | No. It's missing from the current template (D-1). The grading ruling is still open (Q5) | 26 Nov (comparison) |
