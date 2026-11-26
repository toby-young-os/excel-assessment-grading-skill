#!/usr/bin/env python3
"""Build the test set: anonymise each selected submission and write verdicts.csv.

Inputs (all PRIVATE, never committed):
    MANIFEST.tsv   id, row, group, held_back, method, original_title, extra_names ('|'-separated)
    FORM.xlsx      scoring-form export ("Form Responses 1")
    ORIGINALS/     row-<row>.xlsx, one per manifest row
    staff.txt      coordinator names to scrub from comments (next to the manifest)
    reviewers.tsv  reviewer code <-> name, created/reused next to the manifest

Outputs:
    tests/inputs/submissions/<id>.xlsx (+ .report.json)   git-ignored
    tests/inputs/verdicts.csv                              committed: no candidate names

Prints counts and PASS/CHECK only, never names.

Usage:
    python3 -I build_test_set.py MANIFEST.tsv FORM.xlsx ORIGINALS_DIR TEMPLATE.xlsx OUT_SUBMISSIONS_DIR VERDICTS.csv
"""
import csv
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def detect_route(path: Path) -> dict:
    """What the file can support, from markers inside it (see notes/test-set-plan.md §4)."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    core = z.read("docProps/core.xml").decode("utf-8", "ignore") if "docProps/core.xml" in names else ""
    app = z.read("docProps/app.xml").decode("utf-8", "ignore") if "docProps/app.xml" in names else ""
    pivots = sum(1 for n in names if re.match(r"xl/pivotTables/pivotTable\d+\.xml$", n))
    records = sum(1 for n in names if re.match(r"xl/pivotCache/pivotCacheRecords\d+\.xml$", n))
    charts = sum(1 for n in names if re.match(r"xl/charts/chart\d+\.xml$", n))
    chart_pics = sum(1 for n in names if re.match(r"xl/media/Chart\d+\.png$", n))
    has_author = bool(re.search(r"<(?:\w+:)?(creator|lastModifiedBy)>[^<]+<", core))
    excel_app = "Microsoft" in app
    if not has_author and not excel_app:
        route = "google-sheets-export"
    elif chart_pics:
        route = "excel-via-google (charts as pictures)"
    else:
        route = "native-excel"
    return {"route": route, "pivot_tables": pivots, "pivot_records": records,
            "chart_objects": charts, "chart_pictures": chart_pics}


def scrub(text: str, names: list) -> str:
    """Replace candidate names (full, first, last, whole word) in reviewer comments."""
    if not isinstance(text, str) or not text.strip():
        return ""
    out = text
    parts = set()
    for n in names:
        out = re.sub(r"(?<![A-Za-z])" + r"[\s,]+".join(map(re.escape, n.split())) + r"(?![A-Za-z])",
                     "[CANDIDATE]", out, flags=re.I)
        parts |= {p for p in re.split(r"[\s,]+", n) if len(p) >= 2}
    for p in sorted(parts, key=len, reverse=True):
        out = re.sub(r"(?<![A-Za-z])" + re.escape(p) + r"(?![A-Za-z])", "[CANDIDATE]", out, flags=re.I)
    out = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]", out)
    return re.sub(r"\s+", " ", out).strip()


# ---------------------------------------------------------------------------
# Reviewer pseudonyms, staff names, gendered pronouns, other identifying details
# ---------------------------------------------------------------------------
def load_coordinators(path: Path) -> list:
    """Coordinator/staff names (not reviewers) to scrub from comments, one per line.
    Kept PRIVATE (git-ignored) so no staff names live in the code."""
    if not path.exists():
        print(f"WARNING: {path} not found; coordinator names will not be scrubbed from comments")
        return []
    return [l.strip() for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]

# Words that typically FOLLOW an object pronoun ("gave her a 3", "told her to ...", "her.").
# If "her" is followed by one of these (or punctuation/end), it is treated as an object pronoun;
# otherwise as a possessive ("her answer" -> "the candidate's answer").
OBJECT_FOLLOWERS = {
    "a", "an", "the", "to", "and", "or", "but", "in", "on", "for", "with", "at", "as", "that",
    "this", "which", "if", "because", "so", "about", "from", "by", "of", "into", "than", "then",
    "credit", "points", "point", "full", "partial", "some", "more", "less", "any", "no", "back",
    "up", "out", "is", "was", "be", "been", "being", "were", "are", "will", "would", "should",
    "could", "can", "may", "might", "has", "had", "have", "did", "does", "do", "not",
}


def match_case(src: str, repl: str) -> str:
    return repl[0].upper() + repl[1:] if src[:1].isupper() else repl


def degender(text: str, sid: str, flags: list) -> tuple:
    """he/she/him/his/her/hers/himself/herself -> 'the candidate' forms. Returns (text, counts)."""
    counts = {}

    def bump(k):
        counts[k] = counts.get(k, 0) + 1

    def sub(pattern, repl, label, flag=False):
        nonlocal text

        def f(m):
            bump(label)
            if flag:
                s = max(0, m.start() - 40); e = min(len(text), m.end() + 40)
                flags.append(f"{sid}: ...{text[s:e]}... ({label})")
            return match_case(m.group(0), repl)
        text = re.sub(pattern, f, text, flags=re.I)

    # Contractions first ("she's" could be "she is" or "she has": flagged).
    sub(r"\b(?:he|she)'s\b", "the candidate's", "he's/she's", flag=True)
    sub(r"\b(?:he|she)'d\b", "the candidate'd", "he'd/she'd", flag=True)
    sub(r"\b(?:he|she)'ll\b", "the candidate will", "he'll/she'll")
    sub(r"\b(?:himself|herself)\b", "themselves", "himself/herself")
    sub(r"\bhers\b", "the candidate's", "hers")
    sub(r"\bhis\b", "the candidate's", "his")
    sub(r"\bhim\b", "the candidate", "him")

    # "her": possessive vs object, decided by the next word.
    out, pos = [], 0
    for m in re.finditer(r"\bher\b", text, flags=re.I):
        after = text[m.end():]
        nm = re.match(r"\s+([A-Za-z]+)", after)
        nxt = nm.group(1) if nm else None
        if nxt is None or nxt.lower() in OBJECT_FOLLOWERS:
            repl, label = "the candidate", "her (object)"
        else:
            repl, label = "the candidate's", "her (possessive)"
            if nxt.lower().endswith(("ed", "ly")):      # e.g. "her explained ..." is unusual: flag
                flags.append(f"{sid}: ...{text[max(0, m.start()-40):m.end()+40]}... (her, unsure)")
        bump(label)
        out.append(text[pos:m.start()] + match_case(m.group(0), repl)); pos = m.end()
    text = "".join(out) + text[pos:]

    sub(r"\b(?:he|she)\b", "the candidate", "he/she")
    sub(r"\b(?:Mr|Mrs|Ms|Miss|Mx)\.?\s+(?:\[CANDIDATE\]|[A-Z][a-z]+)", "[CANDIDATE]", "title + name")
    return text, counts


def scrub_staff(text: str, staff: dict) -> tuple:
    """Staff names (reviewers, coordinators) in comments -> reviewer code or [STAFF]."""
    n = 0
    for full, code in sorted(staff.items(), key=lambda kv: -len(kv[0])):
        for variant in {full, full.split()[0]}:
            if len(variant) < 3:
                continue
            text, k = re.subn(r"(?<![A-Za-z])" + re.escape(variant) + r"(?:'s)?(?![A-Za-z])", code, text, flags=re.I)
            n += k
    return text, n


SCAN = {
    "university/college/school": r"\b(?:university|college|univ\.?|school|institute)\b",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"\+?\d[\d\s().-]{8,}\d",
    "url/linkedin": r"https?://|www\.|linkedin",
    "employer words": r"\b(?:worked at|works at|employer|internship at|intern at|currently at)\b",
}


def main():
    manifest, form, originals, template, out_dir, verdicts = sys.argv[1:7]
    reviewer_map = Path(sys.argv[7]) if len(sys.argv) > 7 else Path(manifest).with_name("reviewers.tsv")
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(form, "Form Responses 1")
    df = df[df.iloc[:, 0].notna()].reset_index(drop=True)
    df["row"] = df.index + 2
    c = df.columns
    score_cols = [c[i] for i in (4, 6, 8, 10, 12, 14)]
    comment_cols = [c[i] for i in (5, 7, 9, 11, 13, 15)]
    other_col = c[17]

    # Reviewer pseudonyms: stable across rebuilds (mapping kept PRIVATE next to the manifest).
    codes = {}
    if reviewer_map.exists():
        codes = {r["reviewer"]: r["code"] for r in csv.DictReader(open(reviewer_map), delimiter="\t")}
    man_rows = sorted(csv.DictReader(open(manifest), delimiter="\t"), key=lambda x: x["id"])
    for m in man_rows:   # assign new codes in submission-ID order (not alphabetical, not by group)
        name = str(df[df.row == int(m["row"])].iloc[0][c[2]]).strip()
        if name not in codes:
            codes[name] = f"reviewer-{len(codes) + 1:02d}"
    with open(reviewer_map, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["code", "reviewer"])
        for name, code in sorted(codes.items(), key=lambda kv: kv[1]):
            w.writerow([code, name])
    staff = dict(codes)
    coordinators = load_coordinators(Path(manifest).with_name("staff.txt"))
    for name in set(df[c[2]].astype(str).str.strip()) | set(coordinators):
        staff.setdefault(name, "[STAFF]")

    flags, pron_counts, staff_hits, scan_counts, scan_flags = [], {}, 0, {}, []

    def clean(txt, names, sid):
        nonlocal staff_hits
        t = scrub(txt, names)
        if not t:
            return ""
        t, k = scrub_staff(t, staff); staff_hits += k
        t, cnt = degender(t, sid, flags)
        for key, v in cnt.items():
            pron_counts[key] = pron_counts.get(key, 0) + v
        for label, pat in SCAN.items():
            for mm in re.finditer(pat, t, flags=re.I):
                scan_counts[label] = scan_counts.get(label, 0) + 1
                scan_flags.append(f"{sid}: ...{t[max(0, mm.start()-40):mm.end()+40]}... ({label})")
        return t

    rows_out, results = [], []
    for m in man_rows:
        r = df[df.row == int(m["row"])].iloc[0]
        names = [str(r[c[3]]).strip()] + [n for n in m["extra_names"].split("|") if n.strip()]
        src = Path(originals) / f"row-{m['row']}.xlsx"

        cmd = [sys.executable, "-I", str(HERE / "anonymise_xlsx.py"), str(src), str(out_dir),
               "--id", m["id"], "--template", template, "--source-name", m["original_title"]]
        for n in names:
            cmd += ["--name", n]
        res = subprocess.run(cmd, capture_output=True, text=True)
        verdict = "PASS" if "RESULT: PASS" in res.stdout else "CHECK"
        rep = json.load(open(out_dir / f"{m['id']}.report.json")) if (out_dir / f"{m['id']}.report.json").exists() else {}
        route = detect_route(out_dir / f"{m['id']}.xlsx") if verdict == "PASS" else {}
        results.append((m["id"], m["group"], verdict, rep, route, res.stderr.strip()[-200:]))

        scores = [r[sc] for sc in score_cols]
        num = pd.to_numeric(pd.Series(scores), errors="coerce")
        row = {
            "id": m["id"], "group": m["group"], "held_back": "yes" if m["held_back"] == "1" else "no",
            "review_month": pd.to_datetime(r[c[0]]).strftime("%Y-%m"),
            "reviewer": codes[str(r[c[2]]).strip()],
            "source": m["method"], "route_detected": route.get("route", ""),
            "pivot_tables": route.get("pivot_tables", ""), "pivot_records": route.get("pivot_records", ""),
            "chart_objects": route.get("chart_objects", ""), "chart_pictures": route.get("chart_pictures", ""),
        }
        for i in range(6):
            v = num.iloc[i]
            row[f"q{i+1}_score"] = "" if pd.isna(v) else (int(v) if float(v).is_integer() else float(v))
        row["total"] = num.sum() if num.notna().all() else ""
        row["recommendation"] = str(r[c[16]]).strip()
        for i in range(6):
            txt = r[comment_cols[i]]
            if pd.isna(num.iloc[i]) and isinstance(scores[i], str):   # comment typed into the score cell
                txt = f"{scores[i]} {txt if isinstance(txt, str) else ''}"
            row[f"q{i+1}_comment"] = clean(txt, names, m["id"])
        row["other_comments"] = clean(r[other_col], names, m["id"])
        rows_out.append(row)

    rows_out.sort(key=lambda x: x["id"])
    with open(verdicts, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader(); w.writerows(rows_out)

    # Console: IDs, groups and outcomes only.
    for sid, g, v, rep, route, err in sorted(results):
        extra = f" | images {rep.get('extra_images', 0)} (OCR hits {rep.get('ocr_hits', 0)})" if rep else ""
        print(f"{sid} {g:<10} {v} | {route.get('route', '-')}{extra}" + (f" | ERR {err}" if err and v != "PASS" else ""))
    print(f"\n{sum(1 for x in results if x[2] == 'PASS')}/{len(results)} PASS; verdicts -> {verdicts}")
    print(f"reviewers pseudonymised: {len(set(r['reviewer'] for r in rows_out))} codes (mapping -> {reviewer_map})")
    print(f"staff names replaced in comments: {staff_hits}")
    print(f"pronouns replaced: {pron_counts or 'none'}")
    print(f"scan for other identifying details: {scan_counts or 'none'}")
    for f_ in flags + scan_flags:
        print("  FLAG", f_)


if __name__ == "__main__":
    sys.exit(main())
