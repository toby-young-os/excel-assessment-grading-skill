#!/usr/bin/env python3
"""Recompute the expected answers from the candidate's OWN raw data and compare with what they submitted.

Usage:  python3 -I verify_candidate.py <candidate.xlsx>
Needs:  pandas, openpyxl.   Output is plain text for the grader (Claude) to interpret, not to paste to the user.

Why recompute from the candidate's own raw data (Monthly Data cols A:E + cma_lkup) rather than only using the key:
if a candidate altered data or mis-pasted it, the key's numbers would hide it.
Rounding differences are never errors; TOL is far looser than any display rounding.
"""
import sys, os, re, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *
import pandas as pd

f = sys.argv[1]; SP = "Sprint Wireless"; TOL = 1e-4
z = zipfile.ZipFile(f)
wb = openpyxl.load_workbook(f); wv = openpyxl.load_workbook(f, data_only=True)
ans = find_answers_sheet(wb.sheetnames)

# ---------- raw data + expected answers
md = pd.read_excel(f, sheet_name="Monthly Data", usecols="A:E")
lk = pd.read_excel(f, sheet_name="cma_lkup"); lk.columns = ["cma_id", "region", "Subregion", "pops"]
d = md.merge(lk, on="cma_id", how="left")
share = lambda x: x[x.Winner == SP].Wins.sum() / x.Wins.sum()
mshare = lambda df: df.groupby("Month_Year").apply(share).tolist()
filt = d[d.region.isin(["Northeast", "MidWest"]) & (d.pops > 500000)].copy(); filt["q"] = filt.Month_Year.dt.quarter
regiononly = d[d.region.isin(["Northeast", "MidWest"])]
E = {"q1_rows": len(filt)}
E["overall_client"] = mshare(filt)
ne = filt[filt.region == "Northeast"]; mw = filt[filt.region == "MidWest"]
aug = ne[ne.Month_Year == "2014-08-01"].groupby("cma_name").apply(share).sort_values()
jul = ne[ne.Month_Year == "2014-07-01"].groupby("cma_name").apply(share)
E["q3"] = list(aug.head(5).items())
E["q4"] = [(k, float(jul[k]), float(aug[k]), float(aug[k] / jul[k] - 1)) for k in aug.head(5).index]
q5 = mw.groupby("Subregion").apply(lambda x: pd.Series({"2Q": share(x[x.q == 2]), "3Q": share(x[x.q == 3])})); q5["pct"] = q5["3Q"] / q5["2Q"] - 1
E["q5_best"] = q5["3Q"].idxmax(); E["q5"] = q5.loc[E["q5_best"]].to_dict()
ny = filt[filt.cma_name.str.startswith("New York, NY")]
refs = {  # known series a candidate might legitimately (or wrongly) plot, by month
    "Sprint monthly, client-filtered (the Q1 'overall')": E["overall_client"],
    "Sprint monthly, UNFILTERED nationwide": mshare(d),
    "Sprint monthly, region-only (no population filter)": mshare(regiononly),
    "Sprint monthly, Northeast only (pop>500k)": mshare(ne),
    "Sprint monthly, Midwest only (pop>500k)": mshare(mw),
    "NY CMA Sprint monthly": mshare(ny),
    "NY CMA minus client-filtered overall": [a - b for a, b in zip(mshare(ny), E["overall_client"])],
}
sets = {"NY carrier shares 2014": sorted(ny.groupby("Winner").Wins.sum().div(ny.Wins.sum()).tolist()),
        "Overall(client) carrier shares 2014": sorted(filt.groupby("Winner").Wins.sum().div(filt.Wins.sum()).tolist())}
cma_names = set(d.cma_name); subregions = set(lk.Subregion)

print("== EXPECTED (recomputed from the candidate's own raw data) ==")
print(" Q1 rows:", E["q1_rows"], "(+1 header = %d); Northeast %d, MidWest %d" % (E["q1_rows"] + 1, len(ne), len(mw)))
print(" Q2 monthly:", [round(x, 4) for x in E["overall_client"]])
print(" Q3:", [(k, round(v, 4)) for k, v in E["q3"]])
print(" Q4:", [(k, round(a, 4), round(b, 4), round(c, 4)) for k, a, b, c in E["q4"]])
print(" Q5:", E["q5_best"], {k: round(v, 4) for k, v in E["q5"].items()})
print(" Q6 ref: NY 2014 %.4f | overall(client) 2014 %.4f | NY vs overall %.1f%% | overall vs NY %+.1f%%" % (
      share(ny), share(filt), 100 * (share(ny) / share(filt) - 1), 100 * (share(filt) / share(ny) - 1)))

# ---------- origin / metadata
print("\n== File origin & metadata ==")
gs = sum(1 for s in wb.sheetnames for r in wb[s].iter_rows(max_row=400) for c in r if "__xludf" in str(ftext(c.value)))
print(" Google Sheets export markers (__xludf) in first 400 rows of each tab:", gs, "-> built/saved in Google Sheets" if gs else "")
if "docProps/core.xml" in z.namelist():
    x = rd(z, "docProps/core.xml")
    for t in ("creator", "lastModifiedBy", "created", "modified"):
        m = re.search(rf"<(?:\w+:)?{t}[^>]*>(.*?)</", x); print(f" {t}: {m.group(1) if m else None}")
print(" app.xml present:", "docProps/app.xml" in z.namelist(), "(absent usually means re-saved by a non-Excel tool)")

# ---------- sheet profiles (hidden rows / filters / population scope) for sheets holding the dataset
def profile(name):
    ws = wb[name]; path = dict(sheet_paths(z))[name]
    x = rd(z, path); af = re.findall(r"<autoFilter\b.*?(?:/>|</autoFilter>)", x, flags=re.S)
    try: df = pd.read_excel(f, sheet_name=name).dropna(how="all")
    except Exception as e: return {"error": str(e)}
    cols = {str(c).strip().lower(): c for c in df.columns}
    def pick(*keys, exclude=()):
        for k, c in cols.items():
            if any(k.startswith(p) for p in keys) and not any(e in k for e in exclude): return c
    rc = pick("region", exclude=("sub",)); pc = pick("pop"); sc = pick("subregion", "sub region", "sub_region"); mc = pick("month"); ic = pick("cma_id"); wc = pick("winner"); ec = pick("wins")
    hidden = [r for r in range(2, len(df) + 2) if ws.row_dimensions[r].hidden]
    vis_idx = [i for i in range(len(df)) if (i + 2) not in set(hidden)]
    p = dict(rows=len(df), hidden=len(hidden), visible=len(vis_idx), has_subregion=sc is not None, cols=list(df.columns), autofilter=[a[:200] for a in af],
             regions=df[rc].value_counts().to_dict() if rc else None, min_pop=df[pc].min() if pc else None)
    if hidden and pc:
        v = df.iloc[vis_idx]; p["visible_min_pop"] = v[pc].min(); p["visible_regions"] = v[rc].value_counts().to_dict() if rc else None
    p["df"], p["vis_idx"], p["keys"] = df, vis_idx, (mc, ic, wc, ec)
    return p

print("\n== Q1: Workbook 1 ==")
if "Workbook 1" in wb.sheetnames:
    p = profile("Workbook 1")
    if "error" in p: print(" could not read:", p["error"])
    else:
        print(f" rows with data: {p['rows']} | hidden by filter: {p['hidden']} | visible: {p['visible']} | expected {E['q1_rows']}")
        print(" columns:", p["cols"]); print(" SubRegion column present:", p["has_subregion"], "(needed for Q5)")
        print(" regions (all rows):", p["regions"], "| min population (all rows):", p["min_pop"])
        if p["hidden"]: print(" HIDDEN-ROW FILTER in use -> visible regions:", p.get("visible_regions"), "| visible min pop:", p.get("visible_min_pop"), "| autofilter:", p["autofilter"])
        mc, ic, wc, ec = p["keys"]
        if all([mc, ic, wc, ec]):
            df = p["df"]; a = filt.assign(m=filt.Month_Year.astype(str)).set_index(["m", "cma_id", "Winner"]).Wins.round(2)
            def keyset(frame):
                t = frame.assign(m=pd.to_datetime(frame[mc]).astype(str)); return t.set_index(["m", ic, wc])[ec].round(2)
            for lab, frame in [("all rows", df), ("visible rows", df.iloc[p["vis_idx"]])]:
                if lab == "visible rows" and not p["hidden"]: continue
                b = keyset(frame)
                print(f" {lab}: missing vs expected {len(a.index.difference(b.index))} | extra {len(b.index.difference(a.index))} | duplicates {int(b.index.duplicated().sum())}")
else: print(" no Workbook 1 tab")

# ---------- pivot map
print("\n== Pivot tables: where each one gets its data ==")
PV = pivots_by_sheet(z); src_profiles = {}
if not PV: print(" NO PIVOT TABLES in the workbook (Resources tab links to pivot tutorials)")
for sh, lst in PV.items():
    for pv in lst:
        n_vals = 0
        if pv["loc"]:
            c1, r1, c2, r2 = rangebox(pv["loc"]); n_vals = sum(1 for r in range(r1, r2 + 1) for c in range(c1, c2 + 1) if wv[sh].cell(r, c).value is not None)
        s = pv["src"][0] if pv["src"] else None
        print(f" {sh} {pv['loc']}: source={pv['src']} | show-as={pv['showas']} | page filters={pv['pagefields']} | stored output cells={n_vals}" + ("  <-- NO STORED OUTPUT" if n_vals == 0 else ""))
        if s and s in wb.sheetnames and s not in src_profiles:
            q = profile(s); src_profiles[s] = q
            if "error" not in q:
                print(f"    source sheet '{s}': rows {q['rows']}, hidden {q['hidden']}, min pop {q['min_pop']}" + (f", visible min pop {q.get('visible_min_pop')}" if q['hidden'] else "") + f", regions {q['regions']}")
print(" NOTE: a source sheet whose min population is below 500,000 (and has no hidden-row filter) means pivots built on it ignore the client's population filter.")

# ---------- answers sheet: locate tables by header text, compare, and detect scale / ratio-vs-change
def num(x):
    try: return float(x)
    except Exception: return None
def close(x, y):
    x = num(x)
    return x is not None and (abs(x - y) <= TOL or abs(x / 100 - y) <= TOL)   # accept fraction or percent units
print("\n== Answers sheet:", ans, "==")
if ans:
    sh = wv[ans]; cells = {}
    for row in sh.iter_rows():
        for c in row:
            if c.value is not None: cells[(c.row, c.column)] = c.value
    def find(pred):
        return sorted(r for (r, c), v in cells.items() if isinstance(v, str) and pred(v.strip().lower()))
    h_mkt = find(lambda s: s.startswith("market (cma)")); h_sub = find(lambda s: s.startswith("subregion") or s == "sub region")
    def table(hr, ncols, maxrows=8):
        rows = []
        for r in range(hr + 1, hr + 1 + maxrows):
            vals = [cells.get((r, c)) for c in range(2, 2 + ncols)]
            if all(v is None for v in vals): break
            if isinstance(vals[0], str) and re.match(r"^\d\)", vals[0].strip()): break
            rows.append(vals)
        return rows
    def kind(name):
        n = str(name).strip()
        return "CMA" if n in cma_names else ("SubRegion" if n in subregions else "other/unrecognised")
    ratio_hits = 0
    if h_mkt:
        t3 = table(h_mkt[0], 2); print(f" Q3 table (header row {h_mkt[0]}): {len(t3)} rows")
        exp3 = dict(E["q3"])
        for n, v in t3: print(f"   {n!r} [{kind(n)}] value={v} | in expected five: {str(n).strip() in exp3} | value ok: {close(v, exp3.get(str(n).strip(), -9))}")
        print("   expected five:", [k for k, _ in E["q3"]])
    if len(h_mkt) > 1:
        t4 = table(h_mkt[1], 4); print(f" Q4 table (header row {h_mkt[1]}): {len(t4)} rows"); exp4 = {k: (a, b, c) for k, a, b, c in E["q4"]}
        for n, jv, av, pc in t4:
            e = exp4.get(str(n).strip())
            ok = e and close(jv, e[0]) and close(av, e[1]) and close(pc, e[2])
            note = ""
            if e and num(jv) and num(av) and num(pc) is not None:
                ratio = num(av) / num(jv)
                if abs(num(pc) - ratio * 100) < 0.1 or abs(num(pc) - ratio) < 1e-3: note = "  <-- % CHANGE REPORTED AS A RATIO (new/old), NOT (new-old)/old"; ratio_hits += 1
            print(f"   {n!r} [{kind(n)}] jul={jv} aug={av} change={pc} | row ok: {bool(ok)}{note}")
        print("   expected:", [(k, round(a, 4), round(b, 4), round(c, 4)) for k, a, b, c in E["q4"]])
    if h_sub:
        t5 = table(h_sub[0], 4, 4); print(f" Q5 table (header row {h_sub[0]}):")
        for n, a, b, c in t5:
            note = ""
            if num(a) and num(b) and num(c) is not None and (abs(num(c) - num(b) / num(a) * 100) < 0.1 or abs(num(c) - num(b) / num(a)) < 1e-3): note = "  <-- % CHANGE REPORTED AS A RATIO"; ratio_hits += 1
            print(f"   {n!r} [{kind(n)}] 2Q={a} 3Q={b} change={c} | winner ok: {str(n).strip() == E['q5_best']} | values ok: {close(a, E['q5']['2Q']) and close(b, E['q5']['3Q']) and close(c, E['q5']['pct'])}{note}")
        print("   expected:", E["q5_best"], {k: round(v, 4) for k, v in E["q5"].items()})
    if not h_mkt and not h_sub: print(" Could not find the answer tables by header text - read the dump (all Answers cells are listed there).")
    nform = sum(is_formula(c.value) for r in wb[ans].iter_rows() for c in r)
    print(f" formulas on the answers tab: {nform} (links to Workbook tabs are good practice; typed numbers are worth a look but not an error by themselves)")
    if ratio_hits: print(f" !! percent-change-as-ratio found in {ratio_hits} answer row(s) - repeated conceptual error if in more than one place")

# ---------- every chart series, resolved from the cells it points at (many files have no stored chart cache)
print("\n== Charts: each series vs recomputed references ==")
seen = {}
for n in sorted(x for x in z.namelist() if re.match(r"xl/charts/chart\d+\.xml", x)):
    cx = rd(z, n)
    ttl = ["".join(re.findall(r"<a:t>(.*?)</a:t>", t)) for t in re.findall(r"<c:title>.*?</c:title>", cx, flags=re.S)]
    kinds = re.findall(r"<c:(lineChart|barChart|pieChart|areaChart|scatterChart|bar3DChart|doughnutChart)>", cx)
    for s in re.findall(r"<c:ser>.*?</c:ser>", cx, flags=re.S):
        fr = [r.replace("&amp;", "&").replace("&apos;", "'") for r in re.findall(r"<c:f>(.*?)</c:f>", s)]
        key = (tuple(fr), tuple(ttl))
        if key in seen: seen[key].append(n); continue
        seen[key] = [n]
        v = [num(x) for x in resolve_range(wv, fr[-1])] if fr else []
        v = [x for x in v if x is not None]
        hit = []
        for k, r in refs.items():
            if len(v) == len(r) and (all(abs(x - y) < TOL for x, y in zip(v, r)) or all(abs(x / 100 - y) < TOL for x, y in zip(v, r))): hit.append(k)
        sv = sorted(v)
        for k, r in sets.items():
            if len(sv) == len(r) and all(abs(x - y) < TOL for x, y in zip(sv, r)): hit.append(k + " (any order)")
        flat = len(v) >= 6 and (max(v) - min(v)) < 0.02 * (abs(sum(v) / len(v)) or 1) * 10 and 0.18 < abs(sum(v) / len(v)) / (100 if sum(v) / len(v) > 1 else 1) < 0.22
        print(f" {n} {kinds} title={ttl} | refs={fr[:3]} | n={len(v)} | matches: {hit or 'none of the standard references (verify by hand)'}" + ("  <-- FLAT near 20% = 1/5 of carriers, not a carrier-specific share" if flat else ""))
        if not hit: print("     values:", [round(x, 4) for x in v][:14])
dups = {k: v for k, v in seen.items() if len(v) > 1}
print(f" {len(seen)} distinct chart series; charts sharing an identical series: {[v for v in dups.values()]}" if dups else f" {len(seen)} distinct chart series")
if len({tuple(k[0]) for k in seen}) == 1 and len(seen) >= 1 and len([n for n in z.namelist() if re.match(r'xl/charts/chart\d+\.xml', n)]) > 1:
    print(" NOTE: every chart plots the same series - the Q6 comparison charts may be missing or collapsed on export; check the original.")

# ---------- formula audit
print("\n== Formula / hardcode audit (pivot output ranges excluded) ==")
for s in wb.sheetnames:
    if (s.startswith("Workbook") and s != "Workbook 1") or s == ans:   # Workbook 1 is pasted data by design
        sh = wb[s]; boxes = [rangebox(p["loc"]) for p in PV.get(s, []) if p["loc"]]
        nf = nc = 0; cons = []
        for row in sh.iter_rows():
            for c in row:
                if is_formula(c.value): nf += 1
                elif isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    if any(b[0] <= c.column <= b[2] and b[1] <= c.row <= b[3] for b in boxes): continue
                    nc += 1; cons.append(c.coordinate)
        print(f" {s}: formulas={nf} | typed numeric constants outside pivots={nc} {cons[:10]}")
fl = [(len(ftext(c.value)), s, c.coordinate, ftext(c.value)) for s in wb.sheetnames if s != "Monthly Data" for r in wb[s].iter_rows() for c in r if is_formula(c.value)]
fl.sort(reverse=True)
print(" total formulas outside Monthly Data:", len(fl), "| over 150 chars:", sum(1 for x in fl if x[0] > 150))
print(" longest:"); [print("  ", l, s, co, v[:260]) for l, s, co, v in fl[:4]]
fn = {}
for _, _, _, v in fl: 
    for g in re.findall(r"([A-Z][A-Z0-9\.]+)\(", v.replace("_xlfn.", "").replace("_xlws.", "").replace("__xludf.DUMMYFUNCTION", "")): fn[g] = fn.get(g, 0) + 1
print(" functions used outside Monthly Data:", dict(sorted(fn.items(), key=lambda kv: -kv[1])))
mdf = [str(ftext(wb["Monthly Data"][a].value))[:240] for a in ("F2", "G2", "H2", "I2")]
print(" Monthly Data helper formulas (row 2, F:I):", mdf)
print(" pivot tables in workbook:", sum(len(v) for v in PV.values()))
print(" AI-style indicators to weigh (never conclusive): array-function chains (FILTER/CHOOSECOLS/CHOOSEROWS/VSTACK/LET/LAMBDA/SORT/UNIQUE):",
      {k: v for k, v in fn.items() if k in ("FILTER", "CHOOSECOLS", "CHOOSEROWS", "VSTACK", "HSTACK", "LET", "LAMBDA", "SORT", "SORTBY", "UNIQUE", "SPLIT", "TOCOL", "XLOOKUP", "SUMPRODUCT")})
