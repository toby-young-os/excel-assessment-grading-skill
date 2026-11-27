"""Shared helpers for the excel-assessment-grading scripts (pure openpyxl/zipfile, no Excel needed)."""
import re, os, zipfile, warnings
warnings.filterwarnings("ignore")
import openpyxl

def ftext(v):
    """Formula text for normal and array formulas; plain value otherwise."""
    return getattr(v, "text", v)

def is_formula(v):
    t = ftext(v)
    return isinstance(t, str) and t.startswith("=")

def rd(z, n):
    return z.read(n).decode("utf8", "ignore")

def sheet_paths(z):
    """[(sheet name, xml path)] in workbook order."""
    wbx = rd(z, "xl/workbook.xml"); rels = rd(z, "xl/_rels/workbook.xml.rels")
    r = {}
    for m in re.finditer(r"<Relationship\b([^>]*)/?>", rels):
        a = m.group(1); i = re.search(r'Id="([^"]+)"', a); t = re.search(r'Target="([^"]+)"', a)
        if i and t: r[i.group(1)] = t.group(1)
    out = []
    for m in re.finditer(r"<sheet\b([^>]*)/?>", wbx):
        a = m.group(1); n = re.search(r'name="([^"]+)"', a); i = re.search(r'r:id="([^"]+)"', a)
        if n and i:
            t = r[i.group(1)].lstrip("/"); out.append((n.group(1).replace("&amp;", "&"), t if t.startswith("xl/") else "xl/" + t))
    return out

def rels_of(z, path):
    rp = os.path.dirname(path) + "/_rels/" + os.path.basename(path) + ".rels"
    return re.findall(r'Target="([^"]+)"', rd(z, rp)) if rp in z.namelist() else []

def norm(base, t):
    return os.path.normpath(os.path.join(os.path.dirname(base), t)).replace("\\", "/")

def find_answers_sheet(names):
    return next((s for s in names if "answer" in s.lower()), None)

def resolve_range(wv, ref):
    """'Sheet 1'!$A$2:$A$13 -> list of cached cell values (None where empty)."""
    m = re.match(r"^'?(.*?)'?!(.+)$", ref)
    if not m or m.group(1) not in wv.sheetnames: return []
    rng = m.group(2).replace("$", "")
    try:
        cells = wv[m.group(1)][rng]
    except Exception:
        return []
    if not isinstance(cells, tuple): return [cells.value]
    out = []
    for row in cells:
        out.extend([c.value for c in row] if isinstance(row, tuple) else [row.value])
    return out

def rangebox(ref):
    from openpyxl.utils import range_boundaries
    return range_boundaries(ref)

def table_map(z):
    """{table name: (sheet name, ref)} for Excel tables (pivots are often sourced from a named table)."""
    m = {}
    for nm, path in sheet_paths(z):
        for t in rels_of(z, path):
            if "tables/table" in t:
                tx = rd(z, norm(path, t))
                n = re.search(r'<table\b[^>]*?\bname="([^"]+)"', tx); r = re.search(r'<table\b[^>]*?\bref="([^"]+)"', tx)
                if n and r: m[n.group(1)] = (nm, r.group(1))
    return m

def pivots_by_sheet(z):
    """{sheet name: [pivot info dicts]} with source sheet/ref, location, filters, show-as."""
    out = {}; tmap = table_map(z)
    for nm, path in sheet_paths(z):
        for t in rels_of(z, path):
            if "pivotTables/pivotTable" not in t: continue
            pp = norm(path, t); px = rd(z, pp)
            loc = re.search(r'<location ref="([^"]+)"', px)
            src = None
            for ct in rels_of(z, pp):
                if "pivotCacheDefinition" in ct:
                    cx = rd(z, norm(pp, ct))
                    ws = re.search(r"<worksheetSource\b([^>]*)/?>", cx)
                    if ws:
                        a = ws.group(1)
                        sh = re.search(r'sheet="([^"]+)"', a); rf = re.search(r'ref="([^"]+)"', a); na = re.search(r'name="([^"]+)"', a)
                        src = (sh.group(1) if sh else None, rf.group(1) if rf else None, na.group(1) if na else None)
                        if src[0] is None and src[2] in tmap: src = (tmap[src[2]][0], tmap[src[2]][1], src[2])
            fields = re.findall(r"<pivotField\b.*?(?:</pivotField>|/>)", px, flags=re.S)
            axis = {}
            for i, fx in enumerate(fields):
                ax = re.search(r'axis="(\w+)"', fx)
                if ax: axis[i] = (ax.group(1), len(re.findall(r'<item\b[^>]*\bh="1"', fx)))
            out.setdefault(nm, []).append(dict(path=pp, loc=loc.group(1) if loc else None, src=src,
                                               showas=re.findall(r'showDataAs="(\w+)"', px) or ["normal"],
                                               axis=axis, pagefields=len(re.findall(r"<pageField\b", px))))
    return out
