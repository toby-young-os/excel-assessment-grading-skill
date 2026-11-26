#!/usr/bin/env python3
"""Dump everything gradeable from a candidate's Excel-assessment workbook into <outdir>/dump.txt (and stdout).
Usage: python3 -I dump_candidate.py <candidate.xlsx> <outdir>"""
import sys, os, re, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
z = zipfile.ZipFile(src); names = z.namelist()
wb = openpyxl.load_workbook(src); wv = openpyxl.load_workbook(src, data_only=True)
rep = []; P = lambda *a: rep.append(" ".join(str(x) for x in a))

# ---- origin + metadata
allf = 0; sheets_flag = 0
for ws in wb:
    for row in ws.iter_rows(max_row=min(ws.max_row, 3000)):
        for c in row:
            t = ftext(c.value)
            if isinstance(t, str) and t.startswith("="):
                allf += 1
                if "__xludf" in t: sheets_flag += 1
P("== ORIGIN:", "GOOGLE SHEETS EXPORT detected (__xludf.DUMMYFUNCTION wrappers; Sheets-only functions may not exist in desktop Excel)" if sheets_flag else "no Google Sheets markers",
  f"[{sheets_flag} wrapped formulas in the first 3000 rows of each tab]")
for p in ("docProps/core.xml", "docProps/app.xml"):
    P("==", p, ("(missing - file was probably re-saved by a non-Excel tool)" if p not in names else ""))
    if p in names: P(re.sub(r"\s*\|\s*(\|\s*)+", " | ", re.sub(r"<[^>]+>", " | ", rd(z, p)))[:500])

PV = pivots_by_sheet(z)
ans_name = find_answers_sheet(wb.sheetnames)
for nm, path in sheet_paths(z):
    ws = wb[nm]; wsv = wv[nm]
    big = ws.max_row > 400
    P("\n=====SHEET", nm, "| dims", ws.dimensions, "| state", ws.sheet_state)
    x = rd(z, path)
    hid = len(re.findall(r'<row\b[^>]*hidden="1"', x)); af = re.findall(r"<autoFilter\b.*?(?:/>|</autoFilter>)", x, flags=re.S)
    if hid or af: P(f"  [FILTER] hidden rows: {hid} | autofilter: {[a[:260] for a in af]}")
    nform = 0
    for row in ws.iter_rows():
        for c in row:
            if c.value is None: continue
            isf = is_formula(c.value); nform += isf
            if big and nm != ans_name and c.row > 12: continue
            v = wsv[c.coordinate].value
            P(f"  {c.coordinate}: {repr(ftext(c.value))[:420]}" + (f"  => {repr(v)[:60]}" if isf else ""))
    P(f"  [formula cells: {nform}]" + ("  [big sheet: only rows 1-12 shown]" if big and nm != ans_name else ""))
    for t in rels_of(z, path):
        if "drawings/drawing" in t:
            d = norm(path, t); dx = rd(z, d)
            for a in re.findall(r"<xdr:(?:twoCellAnchor|oneCellAnchor|absoluteAnchor).*?</xdr:(?:twoCellAnchor|oneCellAnchor|absoluteAnchor)>", dx, flags=re.S):
                fr = re.search(r"<xdr:from><xdr:col>(\d+)</xdr:col>.*?<xdr:row>(\d+)</xdr:row>", a, flags=re.S)
                txt = "\n".join("".join(re.findall(r"<a:t>(.*?)</a:t>", p)) for p in re.findall(r"<a:p>.*?</a:p>", a, flags=re.S))
                pos = fr.groups() if fr else None
                if "<c:chart" in a: P("  [CHART anchor col,row]", pos)
                elif txt.strip(): P("  [TEXTBOX col,row", pos, "]", txt.strip())
            for ct in rels_of(z, d):
                if "charts/chart" in ct:
                    cp = norm(d, ct); cx = rd(z, cp)
                    kinds = re.findall(r"<c:(lineChart|barChart|pieChart|areaChart|scatterChart|bar3DChart|doughnutChart|radarChart)>", cx)
                    ttl = ["".join(re.findall(r"<a:t>(.*?)</a:t>", t_)) for t_ in re.findall(r"<c:title>.*?</c:title>", cx, flags=re.S)]
                    P("  [CHART FILE]", cp, kinds, "titles:", ttl, "| stored cache:", "<c:numCache>" in cx)
                    for s in re.findall(r"<c:ser>.*?</c:ser>", cx, flags=re.S):
                        refs = re.findall(r"<c:f>(.*?)</c:f>", s)
                        P("     series refs:", refs)
                        for r_ in refs[-1:]:
                            vals = resolve_range(wv, r_.replace("&amp;", "&").replace("&apos;", "'"))
                            P("       values from cells:", [round(v, 4) if isinstance(v, float) else v for v in vals][:14])
    for pv in PV.get(nm, []):
        n_vals = 0
        if pv["loc"]:
            c1, r1, c2, r2 = rangebox(pv["loc"])
            n_vals = sum(1 for r in range(r1, r2 + 1) for c in range(c1, c2 + 1) if wsv.cell(r, c).value is not None)
        P("  [PIVOT]", pv["path"], "at", pv["loc"], "| source:", pv["src"], "| show values as:", pv["showas"],
          "| axes (field idx: axis, hidden items):", pv["axis"], "| page filters:", pv["pagefields"], "| non-empty output cells:", n_vals,
          "(0 = no stored output)" if n_vals == 0 else "")
    for t in rels_of(z, path):
        if "tables/table" in t:
            tx = rd(z, norm(path, t))
            P("  [TABLE]", re.findall(r'<table\b[^>]*?\bname="([^"]+)"', tx)[:1], re.findall(r'<table\b[^>]*?ref="([^"]+)"', tx), "cols:", re.findall(r'<tableColumn\b[^>]*?name="([^"]+)"', tx))
open(os.path.join(out, "dump.txt"), "w").write("\n".join(rep))
print("\n".join(rep))
