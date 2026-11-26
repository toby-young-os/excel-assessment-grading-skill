# #excelassessment channel: summary and extract for the skill build

Read-only extraction from Slack `#excelassessment` (private, channel ID `C066X0ACWAU`). Nothing was posted. Covers the full channel history, from its creation on 17 November 2023 to 20 November 2026, including the substantive threads.

**Privacy note:** candidate names are left out. Threads are referenced by Slack permalink so the submission and its context can be found when building the anonymized test set. Reviewer names (Opensignal staff) are kept, since they matter for calibration.

---

## Part 1: Channel summary

### Purpose

The channel is the assignment desk for grading the Excel take-home exercise sent to Market Research Analyst (MRA) candidates. A coordinator posts each completed submission with a link to the scoring form (a Google Form) and tags a reviewer. The reviewer grades it, submits the form, and replies in the thread (usually "done", sometimes with a recommendation or comments).

### Timeline

| Period | Coordinator | What happened |
|---|---|---|
| Nov 2023 to Dec 2024 | Sophie Bradish (recruiting) | First reviewer pool. Answer guide pinned to the channel (17 Nov 2023). Each candidate had their own pre-filled form link. |
| Jun 2025 to Oct 2025 | Joni Factor | Large MRA hiring rounds. New reviewers trained in pairs (Jul 2025). Reviewers asked to tag Joni "with recommendation" so she could review the scoring. Per-candidate scoring forms still in use. |
| Nov 2025 onward | Lisette Labbe (Joni as backup) | Continuous hiring rounds (Nov to Dec 2025, Feb to Apr 2026, Jun 2026, Aug to Nov 2026). From Nov 2025 a single shared scoring form is used for every candidate. Second reviewer rotation in Feb 2026. |
| Nov 2026 | | Gina Muan and Toby Young added on 25 Nov 2026 for the skill rebuild. |

### Current reviewer pool (Aug to Nov 2026)

Allyson Shick, Cameron Whiteford, Jeremy White, Kayla Wilkins, Megan Schneider, Nizar Sakly and Tijana Cosic. Earlier reviewers include Anna Kerwood, Ethan MacRae, Jacob Sears, Jay (Jason) Frongillo, Minh Huynh, Pierce Snyder, Tony Yu, Sarah Khan and Valentina Salome.

### Volume and process

- Several hundred review requests over the channel's life, consistent with the 240 evaluations Joni cited from the form responses.
- Turnaround expectation (Joni, 10 Nov 2025): acknowledge each assignment; morning requests done by end of business, afternoon requests by noon the next business day; 24 to 48 hours at most (Lisette, Jun and Jul 2026).
- Reviewers are asked to say whether they recommend the candidate (Joni, 10 Nov 2025).
- Reviewer comments are shared with hiring managers before interviews (Lisette, 8 Sep 2026: "it has been very helpful").
- Most thread replies are just "done" or "submitted". The verdicts and comments live in the scoring form, not in Slack.

---

## Part 2: Information relevant to the skill build

### A. Official interpretations of the exercise

These are answers reviewers gave to candidate questions. They are the closest thing to a ruling on how the questions should be read.

1. **"Underperforming" (Q3) means lowest win share; "best performing" (Q5) means highest.** No benchmark or "expected" value is provided, so performance is judged on the observed data. Q4 uses the same five markets as Q3.
   - Cameron Whiteford (5 Nov 2026): "there is no given benchmark so underperforming means lowest win share, and best performing means highest. and for the second question the answer is yes, q4 uses the same 5 markets from q3"
   - Allyson Shick (same thread): the instructions describe the data as observed switching data; no expected data is provided or asked for, so "underperforming" should be read from observed data. "My advice is to take the wording for Q3 and Q5 at face value."
   - [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1793910398404779)
2. **The phrase "defined earlier/elsewhere" refers to win share, not underperformance.** Candidates are expected to work out "underperforming" themselves, and reviewers advise them not to overthink it (Allyson and Lisette, 6 Oct 2026). [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1791300701210719)
3. **Q6 expects at least two comparisons or views.** The instruction says "show comparisons" (plural). Jeremy noted (19 Aug 2026) that all three submissions he had seen gave one graph, and that Allyson docked a point for this in her demo. Allyson: "I normally see 2+ graphs, agree the wording could be clearer." [Message](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1787163750599169)
4. **Win counts are not whole numbers because the data is sampled.** Allyson (23 Oct 2026): Opensignal cannot track every switch in the US, so it uses a sample and filters noise with proprietary algorithms. That is why win share, not raw win volume, is the main competitive metric. [Message](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1792777919284069)
5. **Verbatim first sentence of the instructions** (quoted by Jay Frongillo, 18 Aug 2025): "Your client is a regional strategist focused on Sprint Wireless only in the Northeast and Midwest regions, and seeks to understand if there were markets in those regions that significantly under or over-performed in 2014."

### B. Known problems with the exercise template

1. **Percent-change formula may not render in the Resources tab.** Ethan MacRae (28 Jul 2025) found the proportional-difference formula did not display in his Excel, and the same was true in an earlier submission. He gave a candidate full marks for using simple difference because of this. This conflicts with Joni's 25 Nov 2026 summary that confusing percent change with percentage-point difference is heavily penalized. **Need to confirm whether this was fixed in the current template.** [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1753476803429549)
2. **The first sentence invites the "Sprint-only" filter mistake.** Jay Frongillo (18 Aug 2025) saw a pattern of candidates filtering wrongly and suggested a comma or parentheses after "Sprint Wireless". This matches the "Sprint-only trap" Joni later described as the most common Q1 error. **Unknown whether the wording was changed, or whether the trap is intentional.** [Message](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1755542328115999)
3. **Q6 wording ("comparisons") is seen as unclear** by at least two reviewers (see A3).
4. **One-off data-type issue** (12 Nov 2026): a candidate reported wrong data types after Q3 and an empty pivot table. Allyson said no one else had seen it and it was likely local (a Microsoft outage that day). [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1794515783041399)

### C. How reviewers grade in practice

1. **Shown work matters, but missing work in one place gets benefit of the doubt.** Discussion of 18 Aug 2026 ([thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1787068984952939)):
   - Allyson: a correct answer the candidate cannot explain would get "3" plus a flag for possible AI use or poor explanation, "both things the next reviewer should know".
   - Nizar: if Workbooks 1 to 3 show work but 4 does not, it may be a mistake: "I would put a 3 and make a note". If no workbook shows work, or several are copy-pasted, "I'm making a note like 'Answer was right/wrong, gave a good/bad explanation but no work shown, can't follow instructions'".
   - This implies a numeric per-question score in the form, with 3 used for "correct with a caveat". **The scale itself is not stated in the channel.**
2. **IFERROR in simple formulas is seen as odd.** Cameron noticed it in basic percent-change calculations; Nizar called it unnecessary and said reviewers should use their judgement (18 Aug 2026). This is consistent with Joni's point that over-engineered formulas can raise AI suspicion.
3. **AI-use cases flagged by reviewers:**
   - Aug 2026: Nizar spotted a candidate using AI, and Lisette pointed other reviewers to it as "a good example". **Candidate for the AI-use calibration set.** [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1786453594888009)
   - Dec 2025: Jay Frongillo described a submission as "really fishy": no work shown, answers not on the Answers tab, apparently "generated through some sort of online tool (AI, etc.)". He checked both the Google Sheets and Excel versions to rule out a format problem. [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1765980543812219)
4. **Reviewers want to see pivot tables or formulas, not hardcoded values.** Minh Huynh (Oct 2025) rejected a submission with incorrect answers, "no work shown in sheets to give partial credit to and no use of analysis tools such as Pivot Tables or even Excel formulas". Anna Kerwood (Jul 2025) noted a candidate claimed to use pivot tables, but none were in the file.
5. **Reviewers sometimes take a second pass.** Anna Kerwood (Jul 2025) resubmitted her form after working out how a candidate reached their results.

### D. Verdict rationales (useful for calibration examples)

Short reviewer explanations posted in threads. They show how the dimensions trade off in real decisions.

| Date | Reviewer | Verdict | Stated reason |
|---|---|---|---|
| Jul 2025 | Patrick Baker | Hard to recommend | Best open-ended answers he had seen, polished Excel and writing, but did not filter as instructed and misunderstood win share, so every answer was wrong. "It depends what the company values in MRA candidates: smart & skilled OR precise & takes instruction well." |
| Sep 2025 | Pierce Snyder | "Cautious yes" | Completely incorrect win-share logic in Q2 and Q3, but the remaining calculations were perfect. Escalated to Siobhan Dougherty and Emily Sands to decide. |
| Sep 2025 | Minh Huynh | Recommend | Small hiccups, but thorough answers showing attention to detail. |
| Oct 2025 | Minh Huynh | Do not recommend | Technical answers wrong; no work shown; no pivot tables or formulas. |
| Nov 2025 | Minh Huynh | Do not recommend | Charts hard to understand; win share calculated incorrectly; short answers lacked depth. |
| Nov 2025 | Jay Frongillo | Move forward (with a flag) | Some answers right, some wrong because of method; worth training on pivot tables. Joni: "B2B less technical so maybe a fit." |
| Aug 2025 | Kai Brewer | Recommend | Answered almost perfectly. |
| Jun 2026 | Sarah Khan | Reject | "Knows enough Excel to get by, but struggles with more complex tasks." |

Additional verdicts appear as one-liners ("recommend", "do not recommend") in many review threads; the full set with scores and comments is in the scoring form responses.

### E. File-handling problems that affect grading

1. **Excel and Google Sheets render submissions differently, in both directions.**
   - Jacob Sears (14 Nov 2025): a chart looked "terrible" in Google Sheets but normal after downloading and opening in Excel. He nearly gave a low score and wondered whether candidates were being under-scored. Jay Frongillo confirmed the same.
   - Tony Yu (18 Dec 2025): the opposite case, where a line chart showed in Google Sheets but broke after downloading. His guidance: "If the chart seem off on Excel, we should check against Google Sheet - or check both to start with when grading." Lisette pinned this as a PSA. [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1766068783589449)
   - Lisette (15 Dec 2025): formatting may break because candidates email an .xlsx that she uploads to Google Sheets; reviewers should download the Excel version when unclear.
   - Candidates themselves warn about this (Nov 2025: one shared both a Google Drive link and an Excel attachment because charts and text boxes did not display well in Sheets).
2. **Submissions arrive in many forms:** Google Sheets links, .xlsx attachments, OneDrive links, emailed files, an `.xlsb.xlsx` file, and files up to about 24 MB.
3. **Some links point to the wrong file.** At least one shared link opened the blank master template instead of the candidate's copy (Pierce, Sep 2025), and some early links pointed at the master template with a candidate invited as editor.
4. **Some attached files are 0 bytes** in Slack, so the linked copy is the only usable version.

### F. Caveats for using past verdicts as ground truth

1. **The form verdict may not match the reviewer's intent.** In Jun 2026 a reviewer could not see her submitted form and was unsure whether she had marked "proceed" or "do not proceed"; her final Slack answer was to reject. Lisette then changed the form so reviewers can see their results. [Thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1781014799547249)
2. **Names on forms do not always match the submission** (Arianna Thibodeau, Jul 2025).
3. **Forms changed over time.** Per-candidate pre-filled forms were used from 2023 to about Oct 2025; a single shared form has been used since about Nov 2025. Older evaluations may sit in other response sheets.
4. **Many reviewers with varying calibration.** About 25 people have reviewed over three years, trained by pairing and screen-share demos, so verdicts will vary by reviewer.
5. **Borderline cases are escalated** ("cautious yes" to hiring managers), so the final decision may differ from the reviewer's verdict.

---

## Part 3: Resources found in the channel

| Resource | Where |
|---|---|
| Current scoring form (shared, since Nov 2025) | Google Form linked in every request since Nov 2025 |
| Candidate exercise template ("Opensignal Exercise - Excel Exercise - NEW.xlsx") | Same file ID (`12blUDiUeMe8I7Bd33Tzxb0T3BQjKnpoX`) shared in Sep 2025 and Nov 2026, so the template appears unchanged since at least then |
| Excel exercise answer guide | Pinned to the channel by Joni on 17 Nov 2023 (not located by search; check the channel's pinned items) |
| Confirmed AI-use example | [Aug 2026 thread](https://comlinkdata.slack.com/archives/C066X0ACWAU/p1786453594888009) |
| Past submissions | Linked or attached in each review request; Joni says they are shared with view access for anyone at the company |

---

## Part 4: Open questions raised by the channel

1. Was the Resources-tab percent-change formula fixed? If not, should the skill accept simple difference?
2. Was the instruction sentence that causes the Sprint-only filter mistake reworded, or is the trap intentional?
3. What is the numeric scale in the scoring form, and what does each score mean?
4. Is the 2023 pinned answer guide still current, and does it match the skill's `answer-key.md`?
5. Is two or more Q6 comparisons a firm requirement, given reviewers agree the wording is unclear?
6. Which version (Google Sheets or Excel) should the skill treat as authoritative when they differ?
