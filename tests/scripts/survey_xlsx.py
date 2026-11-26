#!/usr/bin/env python3
"""Survey an .xlsx submission for places personal data could sit.

Prints COUNTS ONLY: never cell values, names, emails, paths or metadata values.
Candidate name tokens are derived internally (from the original filename and the
file's own author fields) and are never printed.

Usage:
    python3 -I survey_xlsx.py <file.xlsx> --source-name "<original filename>"
"""
import argparse
import re
import sys
import zipfile
from collections import Counter

# Words that appear in submission filenames but are not names.
STOPWORDS = {
    "opensignal", "exercise", "excel", "new", "copy", "of", "the", "xlsx", "xlsb",
    "xlsm", "market", "research", "analyst", "workbook", "assessment", "final",
    "submission", "answers", "answer", "performance", "group", "mra", "and", "for",
    "version", "v1", "v2", "draft", "test", "sheet", "sheets", "ia",
}

EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
WIN_PATH = re.compile(rb"[A-Za-z]:\\\\?Users\\\\?[^\\\\<\"]+", re.I)
MAC_PATH = re.compile(rb"/Users/[^/<\"]+")
ONEDRIVE = re.compile(rb"d\.docs\.live\.net|sharepoint\.com|-my\.sharepoint", re.I)
GSHEETS = re.compile(rb"Google Sheets|docs\.google\.com", re.I)


def tokens_from_filename(name: str) -> set:
    base = re.sub(r"\.(xlsx|xlsb|xlsm|xls)$", "", name, flags=re.I)
    base = re.sub(r"\(\d+\)", " ", base)
    parts = re.split(r"[\s_\-.,'’()]+", base)
    out = set()
    for p in parts:
        p = re.sub(r"s$", "", p) if p.lower().endswith("'s") else p
        if len(p) >= 3 and p.lower() not in STOPWORDS and not p.isdigit():
            out.add(p.lower())
    return out


def xml_field(xml: bytes, tag: str) -> bytes:
    m = re.search(rb"<(?:\w+:)?" + tag.encode() + rb"[^>]*>(.*?)</(?:\w+:)?" + tag.encode() + rb">", xml, re.S)
    return m.group(1).strip() if m else b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--source-name", default="", help="original filename (used only to derive name tokens)")
    ap.add_argument("--template", default="", help="blank template .xlsx; its author is staff and is excluded")
    a = ap.parse_args()
    staff = set()
    tpl_vals = set()
    if a.template:
        tz = zipfile.ZipFile(a.template)
        for n in tz.namelist():
            if n.endswith(".xml"):
                tpl_vals |= set(re.findall(rb"<(?:a:|c:|)t(?:\s[^>]*)?>([^<]*)</(?:a:|c:|)t>", tz.read(n)))
        tc = tz.read("docProps/core.xml")
        for tag in ("creator", "lastModifiedBy"):
            staff |= {t.decode("utf-8", "ignore").lower() for t in re.split(rb"[\s._@-]+", xml_field(tc, tag)) if len(t) >= 3}

    z = zipfile.ZipFile(a.path)
    names = z.namelist()
    read = lambda n: z.read(n) if n in names else b""

    print(f"== SURVEY ({len(names)} parts, {sum(i.file_size for i in z.infolist())/1e6:.1f} MB uncompressed)")

    # --- 1. Part inventory by category
    cats = Counter()
    for n in names:
        if n.startswith("xl/worksheets/sheet"): cats["worksheets"] += 1
        elif n.startswith("xl/drawings/drawing"): cats["drawings"] += 1
        elif n.startswith("xl/charts/chart"): cats["charts"] += 1
        elif n.startswith("xl/pivotTables/"): cats["pivotTables"] += 1
        elif n.startswith("xl/pivotCache/pivotCacheDefinition"): cats["pivotCacheDefinitions"] += 1
        elif n.startswith("xl/pivotCache/pivotCacheRecords"): cats["pivotCacheRecords"] += 1
        elif n.startswith("xl/media/"): cats["media"] += 1
        elif re.match(r"xl/comments\d*\.xml", n): cats["comments (legacy)"] += 1
        elif n.startswith("xl/threadedComments/"): cats["threadedComments"] += 1
        elif n.startswith("xl/persons/"): cats["persons"] += 1
        elif n.startswith("xl/externalLinks/externalLink"): cats["externalLinks"] += 1
        elif n.startswith("xl/tables/"): cats["tables"] += 1
        elif n.startswith("customXml/"): cats["customXml"] += 1
        elif n.startswith("xl/revisions/"): cats["revisions"] += 1
        elif n == "xl/connections.xml": cats["connections"] += 1
        elif n.startswith("xl/queryTables/"): cats["queryTables"] += 1
        elif n.startswith("xl/embeddings/"): cats["embeddings (OLE)"] += 1
        elif n.startswith("xl/ctrlProps/") or n.startswith("xl/activeX/"): cats["controls"] += 1
        elif n == "xl/vbaProject.bin": cats["VBA macros"] += 1
    print("\n-- 1. Parts present")
    for k, v in sorted(cats.items()):
        print(f"   {k}: {v}")

    # --- 2. Document properties (field names + non-empty flag + length only)
    print("\n-- 2. Document properties (non-empty fields; values hidden)")
    core, app, custom = read("docProps/core.xml"), read("docProps/app.xml"), read("docProps/custom.xml")
    author_tokens = set()
    for tag in ["creator", "lastModifiedBy", "title", "subject", "description", "keywords", "category"]:
        v = xml_field(core, tag)
        if v:
            print(f"   core.{tag}: present (len {len(v)})")
            if tag in ("creator", "lastModifiedBy"):
                if re.fullmatch(rb"sub-\d+", v):
                    continue  # already anonymised (submission ID)
                for t in re.split(rb"[\s._@-]+", v):
                    if len(t) >= 3 and not t.isdigit(): author_tokens.add(t.decode("utf-8", "ignore").lower())
    for tag in ["Company", "Manager", "Application", "HyperlinkBase"]:
        v = xml_field(app, tag)
        if v: print(f"   app.{tag}: present (len {len(v)})")
    if custom:
        print(f"   custom properties: {len(re.findall(rb'<property ', custom))}")
    print(f"   app.Application hints Google Sheets: {bool(GSHEETS.search(app))}")

    # --- 3. Build the internal token set (never printed)
    fn_tokens = tokens_from_filename(a.source_name) if a.source_name else set()
    generic = {"microsoft", "office", "user", "admin", "owner", "windows", "excel", "google", "sheets", "openpyxl"}
    author_tokens -= staff
    tokens = {t for t in (fn_tokens | author_tokens) if t not in generic and t not in STOPWORDS}
    print(f"\n-- 3. Name tokens derived: {len(fn_tokens)} from filename, {len(author_tokens)} from author fields "
          f"(staff excluded: {len(staff)}), {len(tokens)} used (values hidden)")
    print(f"   filename tokens overlap author tokens: {bool(fn_tokens & author_tokens)}")
    # Whole-word matches = real name occurrences; substring-only = usernames/paths or false positives.
    whole = [re.compile(rb"(?<![A-Za-z])" + re.escape(t).encode() + rb"(?![A-Za-z])", re.I) for t in tokens]
    sub = [re.compile(re.escape(t).encode(), re.I) for t in tokens]

    # --- 4. Token, email and path hits per part (counts only)
    print("\n-- 4. Hits per part (name whole-word / name inside a longer word / emails / user paths / cloud URLs)")
    total = Counter()
    for n in names:
        if not (n.endswith(".xml") or n.endswith(".rels") or n.endswith(".vml")):
            continue
        b = z.read(n)
        h_name = sum(len(p.findall(b)) for p in whole)
        h_part = sum(len(p.findall(b)) for p in sub) - h_name
        # Hits inside values that are template text/data (e.g. a place name) are not candidate data.
        if tpl_vals and h_name:
            vals = re.findall(rb"<(?:a:|c:|)t(?:\s[^>]*)?>([^<]*)</(?:a:|c:|)t>", b) + re.findall(rb'<s v="([^"]*)"', b)
            h_tpl = sum(len(p.findall(v)) for v in vals if v in tpl_vals for p in whole)
            h_name -= h_tpl
            total.update(in_template=h_tpl)
        h_mail = len(EMAIL.findall(b))
        h_path = len(WIN_PATH.findall(b)) + len(MAC_PATH.findall(b))
        h_od = len(ONEDRIVE.findall(b))
        if h_name or h_part or h_mail or h_path or h_od:
            print(f"   {n}: names={h_name} partial={h_part} emails={h_mail} paths={h_path} cloud={h_od}")
        total.update(names_=h_name, partial=h_part, emails=h_mail, paths=h_path, cloud=h_od)
    print(f"   TOTAL: names={total['names_']} (+{total['in_template']} inside template text/data) "
          f"partial={total['partial']} emails={total['emails']} paths={total['paths']} cloud={total['cloud']}")
    pats = whole

    # --- 5. Specific known locations
    wb = read("xl/workbook.xml")
    sheet_names = re.findall(rb'<sheet [^>]*name="([^"]+)"', wb)
    print("\n-- 5. Specific locations")
    print(f"   sheets: {len(sheet_names)} (sheet names containing a name token: "
          f"{sum(1 for s in sheet_names if any(p.search(s) for p in pats))})")
    print(f"   workbook absPath (x15ac:absPath) present: {b'absPath' in wb}")
    print(f"   defined names: {len(re.findall(rb'<definedName ', wb))}")
    refreshed = sum(len(re.findall(rb'refreshedBy="', z.read(n))) for n in names if 'pivotCacheDefinition' in n)
    print(f"   pivot caches with refreshedBy: {refreshed}")
    authors = sum(len(re.findall(rb'<author>', z.read(n))) for n in names if re.match(r'xl/comments\d*\.xml', n))
    persons = sum(len(re.findall(rb'<person ', z.read(n))) for n in names if n.startswith('xl/persons/'))
    print(f"   comment authors (legacy): {authors}; persons (threaded): {persons}")
    links = sum(len(re.findall(rb'<hyperlink ', z.read(n))) for n in names if n.startswith('xl/worksheets/sheet'))
    mailto = sum(len(re.findall(rb'mailto:', z.read(n))) for n in names if n.endswith('.rels'))
    print(f"   cell hyperlinks: {links}; mailto targets: {mailto}")
    ss = read("xl/sharedStrings.xml")
    print(f"   shared strings: {len(re.findall(rb'<si>', ss))}")
    dtext = sum(len(re.findall(rb'<a:t>', z.read(n))) for n in names if n.startswith('xl/drawings/drawing'))
    print(f"   text runs in drawings (text boxes): {dtext}")
    ctitles = sum(len(re.findall(rb'<c:title>', z.read(n))) for n in names if n.startswith('xl/charts/chart'))
    print(f"   chart titles: {ctitles}")
    media = [n for n in names if n.startswith('xl/media/')]
    print(f"   images: {len(media)} ({', '.join(sorted({m.rsplit('.',1)[-1] for m in media})) or '-'}) "
          f"-> need a manual look if any are not the template logo")
    print(f"   Google Sheets markers anywhere: {any(GSHEETS.search(z.read(n)) for n in names if n.endswith('.xml'))}")


if __name__ == "__main__":
    sys.exit(main())
