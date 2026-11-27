---
name: excel-assessment-grading
description: Grade a candidate's submitted Opensignal Excel exercise (the Sprint win-share / CMA-lookup / pivot-table assessment, Part A, Q1-Q6) against the answer key and flag possible AI use. Use whenever someone uploads a candidate's completed Excel exercise or assessment workbook (often named like "Opensignal Exercise - Excel Exercise - Candidate Name.xlsx", sometimes with a typo or no name at all), or asks to check, grade, review, score, QA or evaluate a candidate's Excel assessment, applicant submission, or take-home - even if they just say "check this candidate's exercise" or "run the Excel assessment on this file".
---

# Excel assessment grading

Market research analysts use a six-question Excel exercise (Sprint win share, CMA lookup, pivots) to screen applicants. This skill checks a submitted workbook against the answer key and reports whether the candidate shows the core skills the role needs. Accuracy matters a lot: a candidate's chances depend on the report, so never state a finding you have not verified in the file, say when something is an inference, and say when something could not be checked.

The reviewer is ultimately deciding **whether the candidate is a good fit or lacks necessary skills**. Four competencies drive that decision: Excel proficiency, attention to detail, instruction following, and conceptual understanding (win share, percent change). Organize everything around them.

Read `references/answer-key.md` first: the exercise setup, expected answers, known traps, alternative baselines, and the candidate file layout.

## Workflow

1. **Locate the file** (in the sandbox usually `/sessions/*/mnt/uploads/`). Work on a copy; never modify the candidate's file. Do not show file paths in the report. If the file name or a typed name inside the workbook identifies the candidate, you may use it as a label; do not guess identities from anything else.
2. **Run the two scripts** from `${CLAUDE_SKILL_DIR}/scripts/` with `python3 -I` (they need pandas and openpyxl; `pip install --break-system-packages pandas openpyxl` if missing). Large files can take 30-90 seconds.
   - `verify_candidate.py <file>` recomputes every expected answer from the candidate's own raw data, then reports: Workbook 1 contents (rows, hidden-row filters, SubRegion column present), where every pivot table gets its data, the answer tables compared to expected (located by header text, so shifted layouts still work), every chart series resolved from the cells it points at, a formula-vs-hardcode audit, formula-complexity indicators, and file origin/metadata.
   - `dump_candidate.py <file> <outdir>` writes `dump.txt` with every non-empty cell and formula on the small tabs and the whole Answers tab, the written answers (text boxes), chart definitions with values, pivot configuration, tables, filters and hidden rows. Read the Answers, Workbook 2-6 and pivot sections.
   If a script fails, fall back to openpyxl/pandas directly; the logic is simple (numbers are in answer-key.md).
3. **Trace, do not just compare.** For each of Q1-Q5, compare to expected, and for every miss follow it backwards to the first wrong step: wrong filter in Q1, a pivot built on a sheet without the filter, wrong denominator, wrong percent-change formula, sorting labels without their values, wrong unit (CMA vs SubRegion). Then decide whether each wrong answer is an original mistake or a downstream consequence, and whether the logic after the slip was sound. The question is "where did they go wrong, and what does it say about them", not just right or wrong.
4. **Check the written answers and Q6** (below).
5. **Check for AI use** (below).
6. **Write the report** in chat (format below). No files unless the user asks.

## Reading the script output correctly

These are the situations the scripts surface; each needs a deliberate interpretation.
- **Hidden-row filters.** A candidate may paste a larger dataset and apply the population or region filter with an AutoFilter, leaving the other rows hidden. Judge the visible rows against expected (the script reports both). Then check which sheet each pivot reads: pivots built on a sheet with hidden rows can still include those rows, so their results may ignore the filter. Compare the pivot's output values with the candidate-scope recomputation to see which scope was actually used, and state it as an inference.
- **Pivot source mapping.** Use the pivot map to see which questions were built on which sheet and whether that sheet respects the client scope (NE + MW, population over 500,000). Do not infer a sheet's contents from its dimensions: oversized source ranges and formatted empty rows are common. Use the script's row counts and min-population profile.
- **No stored output.** Some files (re-saved by non-Excel tools) hold pivot tables and charts with no stored values. If so you cannot read those numbers; recompute what they would show from the source scope, label it as inference, and list it under "Not verified".
- **Google Sheets origin** (`__xludf.DUMMYFUNCTION`, AVERAGE.WEIGHTED, SPLIT): the file was built or saved in Google Sheets. That is context, not an error, but this is an Excel exercise and Sheets-only functions may not run in desktop Excel; mention it neutrally.
- **Missing app/author metadata** usually means the file was re-saved by another tool (or anonymized). Context only.
- **All charts plot the same series**: Q6 charts may be missing or collapsed on export. Say you cannot tell from the file and suggest checking the original.
- **Percent-change-as-ratio** flag: the script detects "% change" values equal to new/old (x100). That is a conceptual error, not display formatting.
- **Entity type** flag: Q3/Q4 answers must be CMAs (markets), Q5 a SubRegion. The script labels each answer name as CMA, SubRegion, or unrecognised.
- **Flat near 20% series**: win share that is nearly constant around 20% (1/5 of five carriers) means the numerator or denominator is not carrier-specific; Sprint's real series runs about 13% to 31%.

## What counts as an error (and what does not)

Not errors: rounding or decimal display; percent shown as 0.138 vs 13.8 (as units, with the right values); order of the five markets; any valid method (pivot vs SUMIFS/FILTER, INDEX/MATCH vs XLOOKUP vs VLOOKUP, helper tabs); answer tab named "Answers (New)" or "Part A - Answers"; 2,656 vs 2,657 rows (header); typed answer cells instead of links; Q5 Midwest-only vs both-regions pivot as long as the winner and Illinois/Wisconsin figures are right.

Real errors, roughly in order of weight:
- **Conceptual:** win share with the wrong denominator or not carrier-specific, shares that cannot sum to 100% (e.g. a 110% win share), percent change computed as a ratio or percentage-point difference, % change divided by the wrong base, quarterly win share built by averaging monthly shares instead of summing wins, "best" chosen by something other than what was asked (3Q14 level, not % change).
- **Excel proficiency:** broken or misaligned lookups, labels sorted without their values (answers attached to the wrong name), pasted numbers where workings should exist, answers that cannot be traced to the Workbook tabs, charts whose data does not match the workings, a filter applied only as hidden rows that downstream work then ignores, no pivot tables at all despite the Resources tab linking to pivot tutorials (note it; it is not by itself an error).
- **Scope/filter slips:** missing population filter, wrong regions, unfiltered nationwide data in Q2 (incorrect, moderate: it ignores the client's specification; check whether it runs into Q6), mixing Northeast and Midwest, wrong month.
- **Instruction following:** SubRegion not appended in Q1 (blocks Q5), answering at the wrong unit (SubRegion or region for Q3/Q4, a CMA for Q5), comparing against the wrong baseline in Q6 (see answer-key), answers not on the Answers tab, work not shown on the named Workbook tab, sub-questions skipped, the Resources tab's definitions ignored.

**Weigh patterns, not single slips.** One missed filter once, with the rest correct, is a human slip: note it plainly and do not dwell. The same kind of mistake in several places (repeated scope slips, repeated misreads of what a question asked, repeated formula errors) is a pattern that says something about core competencies; say so explicitly. Conceptual mistakes and clear Excel-ability gaps are standalone red flags even if they appear once; list them separately and prominently. When one early mistake cascades, report it as one root cause and judge whether the downstream logic was sound given that start. Equally, say when a candidate's fundamentals are right but a sanity check was missed (e.g. a win-share chart flat at 20% left uncorrected). No fixed severity labels or scores; describe what happened and how much it matters in plain words.

## Written answers (3a, 3b, 4a, 4b, 5a)

Quick check only. Does each exist, is it logical and directionally plausible, and does it agree with the candidate's own numbers (3a/4a steps match what the workbook actually does; 4b/5a fit the direction in their data)? Flag incoherent or self-contradictory reasoning, a description that contradicts the workbook, or a claim contradicted by their own chart. Note missing answers. Mention an obvious factual slip only if you are confident, and phrase it as worth verifying. If the logic holds, say nothing more; the reviewer reads them in depth.

## Question 6

No required chart. Check: (1) the comparisons make sense for "compare Sprint's win share in the New York, NY CMA to overall win share (from Q1)": NY vs overall by month, by carrier, deltas, etc.; (2) Workbook 6 numbers actually produce what the charts and captions claim. `verify_candidate.py` matches each chart series to recomputed references (NY CMA, client-filtered overall, nationwide, Northeast-only, Midwest-only...); hand-verify any series marked "none of the standard references". Confirm the CMA is New York, NY (not the NY Metro SubRegion), that "overall" is the Q1 client-filtered dataset (a Northeast-only or nationwide baseline is a different, weaker comparison: say so), formulas link to real workings, annual and quarterly rows use the same numerator and denominator scope, chart titles/labels say what is plotted, and every captioned claim is checked against the numbers (count months above and below; percent claims use the right base and direction). Do not grade against a particular chart, and do not penalize missing commentary (not required), but note a blank text box.

## Checking for AI use

Candidates are told not to use AI (the Instructions tab says so). Flag possible AI use, never decide it: the reviewer makes the call. Give the strongest evidence, or say plainly that you found none. Look for:
- **Excel:** formulas far more complex than the task needs, such as 150-300 character chains of FILTER + CHOOSECOLS/CHOOSEROWS/VSTACK/LET/LAMBDA/SORT/UNIQUE where SUMIFS, a lookup or a pivot would do; unnatural constructions (e.g. deriving a quarter by splitting a date string instead of simple month arithmetic); one cell computing something a pivot gives in two clicks. Simple XLOOKUP/INDEX-MATCH/SMALL and pivots are normal and expected.
- **Mismatch:** sophisticated formulas next to basic conceptual errors or missed sanity checks in the same file is a notable signal. So is a file where some tabs are plain and others suddenly sophisticated.
- **Written answers:** much more industry knowledge than an entry-level applicant would plausibly have (specific carriers' history, spectrum, MVNO economics, regional marketing theory), polished or rigidly structured text ("First... Second... Finally...", "Additionally") where a short answer was asked, generic comprehensive coverage, confident specifics that are wrong or unsupported by the candidate's data.
- **Origin:** a Google Sheets export is context, not evidence on its own.
- **Counter-signals (report them for balance):** informal, specific, slightly rough, data-grounded writing; typos; candid notes about earlier mistakes; simple formulas; steps described in 3a/4a that match the workbook.
Give a concern level (none observed / low / medium / high) with exact quotes or cell references. Metadata (author, last-modified-by, timestamps, missing fields) is context only: report it neutrally if odd, without a conclusion.

## Report format

Chat only, concise, plain language; skip anything that did not need flagging.

1. **Bottom line** (2-4 sentences): the overall picture across the four competencies. No hire/no-hire recommendation and no numeric score.
2. **Scorecard table**, one row per Q1-Q6: Correct or Incorrect (Q6: sensible and accurate, or not). For misses, a short note on what went wrong and whether it is isolated, a cascade, or recurring. For correct answers, just "Correct".
3. **Patterns / root cause**, only if something went wrong: the first wrong step, how it propagated, whether the remaining logic was sound, whether similar mistakes repeat.
4. **Red flags**: conceptual errors and Excel-ability gaps, with evidence ("None" if none).
5. **Written answers**: only anything incoherent or missing; otherwise one line saying they were logical.
6. **AI use**: concern level and strongest evidence (or "no strong indicators" plus the human-authorship signals).
7. **Not verified**: anything you could not check (chart rendering, no stored pivot/chart values, a layout you could not parse, Sheets-only functions, facts from memory) and every conclusion that is an inference.

Be exact with numbers and cell references, and keep a neutral, factual tone toward the candidate.
