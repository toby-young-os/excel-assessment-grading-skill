# excel-assessment-grading

A Claude skill that grades a candidate's completed Opensignal Excel exercise (Part A, Q1–Q6). It traces where mistakes started and acts as a first-pass grader that scores and recommends. The reviewer makes the final decision.

**Status:** rebuild in progress. The materials are gathered and the test set is being built; `SKILL.md` hasn't been written yet. See `notes/` for the current state.

## Layout

| Path | What it holds |
|---|---|
| `excel-assessment-grading/` | The skill itself: `SKILL.md`, `references/`, `scripts/`. Only this folder ships to reviewers |
| `resources/` | Source material the skill is built from (the 2021 answer key) |
| `templates/` | The candidate exercise template, dated; older versions go in `templates/archive/` |
| `tests/inputs/` | Anonymised submissions (`submissions/`, git-ignored) and reviewer verdicts |
| `tests/outputs/` | Skill reports per submission, for comparing with reviewer verdicts |
| `tests/scripts/` | `survey_xlsx.py` (where personal data sits; counts only) and `anonymise_xlsx.py` (replace and verify) |
| `notes/` | Review, knowledge inventory, open questions, template defects, test-set plan; `notes/archive/` holds the Slack extracts |

## Confidential source files (not in the repo)

The exercise template and the 2021 answer key are marked "DO NOT DISTRIBUTE" and are git-ignored. The shipped skill doesn't need them; they're used to build the skill's references and by the test scripts. After cloning, put local copies at the paths below:

| Local path | Source |
|---|---|
| `templates/exercise-template-2026-08-24.xlsx` | [Opensignal Exercise - Excel Exercise - NEW.xlsx](https://docs.google.com/spreadsheets/d/12blUDiUeMe8I7Bd33Tzxb0T3BQjKnpoX/edit) (Google Drive) |
| `resources/answer-key-2021-05-31.xlsx` | `New Excel Exercise (Answer Key) - 05 31 2021.xlsx`. Not in Google Drive; ask Joni Factor for a copy |

## Candidate data rules

This repo is pushed to a shared remote:

- **Never commit candidate submissions**, even anonymised ones. `tests/inputs/submissions/` is git-ignored.
- **Never commit the ID-to-name mapping**, original downloads or raw scoring-form exports. Keep them outside the repo.
- **Anonymise by replacing, never emptying.** Identity fields become the submission ID (`sub-NNN`), and names in text become `[CANDIDATE]`. See `notes/test-set-plan.md` §3.
- **Scripts print counts only.** No one needs to open a candidate's sheet to anonymise it.
- **The template and 2021 answer key are confidential** ("DO NOT DISTRIBUTE") and are git-ignored. See "Confidential source files" above.

## Anonymising a submission

Requires Python 3. `openpyxl`, `pytesseract` and `tesseract` are optional; they're used for the file-opens and image OCR checks.

```bash
python3 -I tests/scripts/survey_xlsx.py IN.xlsx --source-name "<original filename>" \
    --template templates/exercise-template-2026-08-24.xlsx

python3 -I tests/scripts/anonymise_xlsx.py IN.xlsx tests/inputs/submissions --id sub-001 \
    --template templates/exercise-template-2026-08-24.xlsx \
    --source-name "<original filename>" --name "<First Last>"
```

Run both on a copy that sits outside the repo. Each run should end with `RESULT: PASS`.
