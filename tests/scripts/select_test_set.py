#!/usr/bin/env python3
"""Select the test set from the scoring-form export.

Writes the selection, including candidate names, to a PRIVATE csv (keep it outside
git). Prints only IDs, groups, dates and reviewer-cap info, never candidate names.

Plan (notes/test-set-plan.md §2, amended 26 Nov: exactly 20, AI-use cases and
the three hand-graded assessments to be added later). The plan below is left unchanged so the original
selection reproduces; after review the low_yes pick was excluded as an outlier
(score-entry error) and the test set is 19 (see private/excluded.tsv and §2a):

    fail        total 6-11, No       4   (1 held back)
    border_yes  total 12-14, Yes     3   (1)
    border_no   total 12-14, No      3   (1)
    strong      total 15-16, Yes     3   (1)
    top         total 17-18, Yes     3   (1)
    high_no     total >= 15, No      3   (1)
    low_yes     total <= 11, Yes     1   (0)

Rules: prefer reviews on/after the current template date (24 Aug 2026), widening
back in steps only if a group runs short; at most 2 per reviewer across the set;
within "fail", maximise the variety of per-question score patterns. Ranked backups
are kept for each group, for when a submission file can't be found or used.

Usage:
    python3 -I select_test_set.py FORM.xlsx PRIVATE_OUT.csv [--seed 26]
"""
import argparse
import random
import sys

import pandas as pd

PLAN = [  # group, count, held_back
    ("fail", 4, 1), ("border_yes", 3, 1), ("border_no", 3, 1), ("strong", 3, 1),
    ("top", 3, 1), ("high_no", 3, 1), ("low_yes", 1, 0),
]
DATE_STEPS = ["2026-08-24", "2026-07-01", "2026-01-01", "2025-01-01"]
BACKUPS = 3
REVIEWER_CAP = 2


def group_of(total, rec):
    # Half-point totals (e.g. 16.5) fall in the band below.
    if rec == "No":
        if total < 12: return "fail"
        if total < 15: return "border_no"
        return "high_no"
    if total < 12: return "low_yes"
    if total < 15: return "border_yes"
    if total < 17: return "strong"
    return "top"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("form")
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=26)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    df = pd.read_excel(a.form, "Form Responses 1")
    df = df[df.iloc[:, 0].notna()].reset_index(drop=True)
    c = df.columns
    score_cols = [c[i] for i in (4, 6, 8, 10, 12, 14)]
    S = df[score_cols].apply(pd.to_numeric, errors="coerce")
    df["row"] = df.index + 2                       # sheet row number (header = row 1)
    df["date"] = pd.to_datetime(df[c[0]])
    df["reviewer"] = df[c[2]].astype(str).str.strip()
    df["candidate"] = df[c[3]].astype(str).str.strip()
    df["rec"] = df[c[16]].astype(str).str.strip()
    for i, col in enumerate(score_cols, 1):
        df[f"q{i}"] = S[col]
    df["total"] = S.sum(axis=1, min_count=6)
    df = df[df.total.notna() & df.rec.isin(["Yes", "No"])].copy()
    df["group"] = [group_of(t, r) for t, r in zip(df.total, df.rec)]
    df["pattern"] = df[[f"q{i}" for i in range(1, 7)]].apply(
        lambda r: "".join("L" if v <= 1.5 else ("M" if v < 3 else "H") for v in r), axis=1)

    # Same candidate reviewed twice? Keep only the latest review per candidate name.
    df = df.sort_values("date").drop_duplicates("candidate", keep="last")

    per_reviewer = {}
    chosen = []
    # Fill the scarcest groups first so the reviewer cap doesn't starve them.
    pool_size = df.group.value_counts().to_dict()
    for group, n, held in sorted(PLAN, key=lambda p: pool_size.get(p[0], 0)):
        need = n + BACKUPS
        picked = []
        for step in DATE_STEPS:
            pool = df[(df.group == group) & (df.date >= step) & (~df.row.isin([p["row"] for p in picked]))]
            rows = pool.sample(frac=1, random_state=rng.randint(0, 10**6)).to_dict("records")
            if group == "fail":   # variety of score patterns first
                seen, first, rest = set(), [], []
                for r in rows:
                    (first if r["pattern"] not in seen else rest).append(r); seen.add(r["pattern"])
                rows = first + rest
            for r in rows:
                if len(picked) >= need: break
                if per_reviewer.get(r["reviewer"], 0) >= REVIEWER_CAP and len(picked) < n:
                    continue
                picked.append(r)
                if len(picked) <= n:
                    per_reviewer[r["reviewer"]] = per_reviewer.get(r["reviewer"], 0) + 1
            if len(picked) >= need: break
        for k, r in enumerate(picked):
            r["rank"] = "primary" if k < n else f"backup{k - n + 1}"
            r["held_back"] = (k < held) if k < n else ""
            chosen.append(r)

    order = {g: i for i, (g, _, _) in enumerate(PLAN)}
    chosen.sort(key=lambda r: (order[r["group"]], r["rank"] != "primary", r["rank"]))
    out = pd.DataFrame(chosen)[["group", "rank", "held_back", "row", "date", "reviewer", "candidate",
                                "q1", "q2", "q3", "q4", "q5", "q6", "total", "rec", "pattern"]]
    out.to_csv(a.out, index=False)

    # Console: no candidate names.
    print(f"selected {sum(out['rank'] == 'primary')} primary + {sum(out['rank'] != 'primary')} backups -> {a.out}")
    show = out.assign(date=out.date.dt.date, reviewer=out.reviewer.str.split().str[0])
    print(show.drop(columns=["candidate"]).to_string(index=False))
    prim = out[out["rank"] == "primary"]
    print("\nprimary per reviewer:", prim.reviewer.value_counts().to_dict())
    print("primary on/after 24 Aug 2026:", int((prim.date >= "2026-08-24").sum()), "of", len(prim))


if __name__ == "__main__":
    sys.exit(main())
