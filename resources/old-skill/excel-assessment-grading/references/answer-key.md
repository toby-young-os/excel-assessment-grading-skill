# Answer key and known pitfalls (Opensignal Excel exercise, Part A)

Source: the answer-key workbook (2021 template, re-verified by recomputing from the raw data). The scripts recompute
these from each candidate's own raw data, so this file is for interpretation, not for copy-checking.

## Setup
- Data: `Monthly Data` (39,339 rows: Month_Year, cma_id, cma_name, Winner, Wins) + `cma_lkup` (716 rows: cma_id, region, Subregion, pops). 2014, monthly. 5 winners: AT&T, Verizon, Sprint, T-Mobile, All Other Carriers.
- Client scope: Sprint Wireless only; regions **Northeast and MidWest**; **population > 500,000**.
- Win share = carrier wins / all carriers' wins, same geography and period. Percent change = (new - old) / old.
- Quarters: 1Q = Jan-Mar, 2Q = Apr-Jun, 3Q = Jul-Sep, 4Q = Oct-Dec.

## Expected answers
**Q1** - Workbook 1 holds the filtered dataset with Region, SubRegion, Population appended: **2,656 data rows** (2,657 with header). Northeast 1,362 rows, MidWest 1,294. Smallest CMA population 510,541 (no CMA sits exactly at 500,000, so `>` vs `>=` is irrelevant here).

**Q2** - monthly Sprint win share on the **client-filtered** data (not nationwide):
Jan 13.1%, Feb 12.7%, Mar 14.4%, Apr 17.9%, May 22.8%, Jun 23.1%, Jul 13.3%, Aug 23.2%, Sep 29.3%, Oct 30.6%, Nov 26.0%, Dec 28.8%.
Nationwide (unfiltered) would be roughly 11.7%, 11.8%, 13.1%, 15.8%, 19.4%, 19.4%, 11.7%, 19.7%, 25.5%, 27.2%, 23.2%, 24.7% - that is the wrong scope.
Note the July dip (13.3%) between June and August; a good candidate may mention it.

**Q3** - five lowest Sprint win shares among Northeast CMAs (pop > 500k) in Aug 2014 (23 Northeast CMAs qualify):
1. Northeast Pennsylvania, PA - 10.26%
2. New Jersey 2 - Ocean - 12.89%
3. Boston-Lowell-Brockton-Lawrence-Haverhill, MA-NH - 14.42%
4. Long Branch-Asbury Park, NJ - 16.11%
5. Pittsburgh, PA - 16.20%
(Next: Bridgeport 16.37%, Allentown 16.38% - close, so a slightly wrong filter can swap the 5th.)

**Q4** - Jul -> Aug % change for those same five markets (all five improved):
Northeast Pennsylvania 9.02% -> 10.26% = +13.8%; New Jersey 2 - Ocean 10.41% -> 12.89% = +23.9%; Boston 12.91% -> 14.42% = +11.7%; Long Branch 12.37% -> 16.11% = +30.2%; Pittsburgh 12.47% -> 16.20% = +29.9%.
Order may vary. The metric is a *relative* change, not a percentage-point difference (e.g. +3.7 pp for Long Branch would be wrong).

**Q5** - best Midwest SubRegion in 3Q14: **Illinois/Wisconsin**, 3Q14 win share 30.07%, 2Q14 28.59%, change **+5.15%**.
Quarterly win share = sum of Sprint wins / sum of all wins across the quarter's months. Averaging monthly win shares gives a different (wrong) answer: roughly -0.1% for Illinois/Wisconsin.
Other Midwest SubRegions (3Q14 / 2Q14 / change): Michigan/Indiana/KY 28.8% / 24.9% / +15.5%; Kansas/Missouri 23.5% / 23.5% / +0.0%; Pennsylvania/WV/Ohio 23.4% / 18.7% / +25.3%; Great Plains 20.2% / 18.4% / +9.3%.
Trap: "Pennsylvania/WV/Ohio" exists as a SubRegion in both regions (Pittsburgh is Northeast). Without the MidWest filter that SubRegion reads 22.8% / 18.2% / +25.3%. The winner and the Illinois/Wisconsin figures are unaffected, so accept either; only note it if the candidate's winner is wrong or if they ignored the "in the Midwest" instruction in a way that changes the winner. Trap 2: someone who picks the "best" SubRegion by % change (Pennsylvania/WV/Ohio, +25%) instead of by win share level misread "best performing in 3Q14".

**Q6** - open-ended. Reference numbers: NY CMA ("New York, NY-NJ/Nassau-Suffolk, NY/Newark, Jersey City and Paterson-Clifton-Passaic, NJ") 2014 Sprint win share 19.34% vs overall (client-filtered) 22.28%: NY is 13.2% below overall (overall is 15.2% above NY - the old key wrote "NY is 15.2% lower", which is the wrong direction, so judge captions by the math, not by that wording).
NY monthly: 10.5, 11.3, 13.4, 16.4, 20.3, 20.3, 11.3, 20.0, 23.5, 25.7, 23.2, 25.8 (%).
Full-year carrier shares, NY / overall: AT&T 21.1 / 22.5; Verizon 19.7 / 26.2; Sprint 19.3 / 22.3; T-Mobile 34.9 / 24.3; All Other 4.9 / 4.7.

## Written-answer references (quick sanity bar only)
- 3b factors for underperformance: network quality, promotions/pricing vs competitors, demographics differing from Sprint's base, competitor strength/presence.
- 4b why better in August: promotion started or returned to normal after the July dip, seasonality, competitor weakness, network improvement.
- 5a why successful: demographics, network performance, less competition; data to add: coverage maps, pricing/promo history, store counts, demographics.
Anything logical and directionally plausible passes. Flag only incoherent or contradictory reasoning (e.g. explaining a win-share *increase* with something that would hurt Sprint).

## Candidate workbook layout (what the scripts expect)
Tabs: Welcome, Resources, Instructions (New), Answers (New) [older: "Part A - Answers (New)"], cma_lkup, Monthly Data, Workbook 1-6. Answer tables sit at B31:C35 (Q3), B60:E64 (Q4), B89:E89 (Q5); charts and the written answers are drawing objects (text boxes) on the answers tab. Candidates usually add lookup columns to Monthly Data (cols F:H), paste the filtered result in Workbook 1 (often as an Excel table), and build pivots in Workbooks 2-6. Pivot output cells are stored as constants in the file - that is normal and not "hardcoding".

## Reference numbers for recognizing common wrong paths
Use these to identify *which* mistake a wrong number comes from. `verify_candidate.py` recomputes the main ones.

**Q1 columns.** The appended columns should include Region, SubRegion and Population (Q5 needs SubRegion). A dataset without SubRegion cannot answer Q5 at the right level.

**Q2 wrong paths.** Region-only (no population filter) monthly: 12.9, 12.6, 13.9, 16.8, 20.8, 20.7, 12.5, 21.0, 27.7, 29.0, 24.0, 26.2 (%). A series that is flat near 20% (about 20.0-20.5% every month) is not Sprint's share: it comes from using all carriers' wins as the numerator or summing a per-row total into the denominator (about 1/5).

**Q3/Q4 wrong path: SubRegion instead of CMA.** The Northeast has only five SubRegions, so a "top 5" list that is every Northeast SubRegion is the wrong unit. With the population filter, Aug 2014 Sprint win share by Northeast SubRegion: Pennsylvania/WV/Ohio 16.2%, New England 17.8%, Philadelphia Tri-State 18.1%, New York Metro 19.7%, Upstate New York 22.7%; July 2014: 12.5, 12.8, 11.5, 11.3, 11.8 (%). Percent-change-as-ratio looks like 113.78, 123.91, 111.73, 130.17, 129.87 for the five correct markets (Aug/Jul x100) instead of +13.8, +23.9, +11.7, +30.2, +29.9%.

**Q5 wrong paths.** Region-only (no population filter) Midwest SubRegion 2Q14 -> 3Q14: Great Plains 14.2 -> 15.4; Illinois/Wisconsin 25.1 -> 26.5 (+5.7%); Kansas/Missouri 18.7 -> 19.1; Michigan/Indiana/KY 23.0 -> 26.7 (+16.3%); Pennsylvania/WV/Ohio 19.3 -> 23.8 (+23.2%). Answering with a CMA (e.g. Grand Rapids, MI) instead of a SubRegion, averaging monthly shares, or reporting new/old x100 as the change are the other common failures.

**Q6 baselines.** Client-filtered overall 2014 = 22.28% (the Q1 overall). Other baselines are different comparisons and should be called out as such: nationwide unfiltered by month 11.7, 11.8, 13.1, 15.8, 19.4, 19.4, 11.7, 19.7, 25.5, 27.2, 23.2, 24.7 (%); Northeast-only monthly (Jan, Feb, Mar) is 11.6, 12.2, 13.6 with the population filter and 11.3, 11.9, 12.9 without it. NY CMA vs overall must use the NY, NY CMA (cma_id 1), not the New York Metro SubRegion. The annual figure for any regional baseline must use the same numerator and denominator scope (a numerator for NE+MW over a denominator for NE-only gives a bogus ~49%).

## Pivot behaviour worth knowing
Pivots built from a range that has hidden (filtered-out) rows can still include those rows. A candidate who applies the population filter as an AutoFilter on one sheet and then builds pivots from that sheet can end up with region-only results, while pivots built from a different, truly filtered sheet are correct. Always compare a pivot's output values to the recomputed scope to see which was used.
