#!/usr/bin/env python3
"""Anonymise a candidate's .xlsx submission without opening it in Excel or re-saving it.

Policy (agreed 26 Nov 2026, "option C"): identity fields are REPLACED with the
submission ID (e.g. sub-001), never emptied, so the evidence they carry (desktop
Excel vs Google Sheets, pivots refreshed locally, folder/OS) is preserved.

What it does (edits the zip's XML parts in place; every other byte is copied as-is):
  * docProps/core.xml   creator, lastModifiedBy                    -> ID
  * docProps/app.xml    Company, Manager                           -> ID
  * pivot caches        refreshedBy="..."                          -> ID
  * comments / persons  author names, displayName, userId          -> ID
  * workbook.xml        absPath: username segment of the path      -> ID
  * any part            OneDrive/SharePoint personal URL segment   -> ID
  * any part            email addresses                            -> [EMAIL]
  * free text           whole-word candidate names                 -> [CANDIDATE]
                        (shared strings, text boxes, chart titles, comments)
                        Strings that also exist in the blank template are never touched.
  * filename                                                       -> <ID>.xlsx

It prints COUNTS ONLY, never names or values, and then verifies:
  1. every XML part still parses, and the file opens with openpyxl (read-only);
  2. no candidate name token remains (whole word), and no path username remains;
  3. only expected parts changed; worksheets, charts, pivot tables and pivot
     records are byte-identical unless a logged replacement touched them.

Usage:
    python3 -I anonymise_xlsx.py IN.xlsx OUT_DIR --id sub-001 --template TEMPLATE.xlsx \
        --source-name "<original filename>" --name "<First Last>" [--name ...]
"""
import argparse
import io
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

STOPWORDS = {
    "opensignal", "exercise", "excel", "new", "copy", "of", "the", "xlsx", "xlsb", "xlsm",
    "market", "research", "analyst", "workbook", "assessment", "final", "submission",
    "answers", "answer", "performance", "group", "mra", "and", "for", "version", "draft",
    "test", "sheet", "sheets", "microsoft", "office", "user", "admin", "owner", "windows",
    "google", "openpyxl", "apache", "poi",
}
FREE_TEXT = re.compile(r"^xl/(sharedStrings\.xml|drawings/drawing\d+\.xml|charts/chart\d+\.xml|"
                       r"comments\d*\.xml|threadedComments/.*\.xml|drawings/vmlDrawing\d+\.vml)$")
PROTECTED = re.compile(r"^xl/(worksheets/sheet\d+\.xml|charts/chart\d+\.xml|pivotTables/.*\.xml|"
                       r"pivotCache/pivotCacheRecords\d+\.xml|tables/.*\.xml)$")
EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
USER_PATH = re.compile(rb"((?:[A-Za-z]:)?(?:\\\\|\\|/)Users(?:\\\\|\\|/))([^\\/\"<>]+)", re.I)
ONEDRIVE = re.compile(rb"(d\.docs\.live\.net/)([0-9a-fA-F]+)|(-my\.sharepoint\.com/personal/)([^/\"<]+)", re.I)


def split_tokens(s: str, min_len=3):
    s = re.sub(r"\.(xlsx|xlsb|xlsm|xls)$", "", s, flags=re.I)
    s = re.sub(r"\(\d+\)", " ", s)
    out = set()
    for p in re.split(r"[\s_\-.,'’()@]+", s):
        if len(p) >= min_len and p.lower() not in STOPWORDS and not re.fullmatch(r"\d+", p):
            out.add(p.lower())
    return out


def xml_text(xml: bytes, tag: str) -> str:
    m = re.search(rb"<(?:\w+:)?" + tag.encode() + rb"(?:\s[^>]*)?>(.*?)</(?:\w+:)?" + tag.encode() + rb">", xml, re.S)
    return m.group(1).decode("utf-8", "ignore").strip() if m else ""


def set_xml_text(xml: bytes, tag: str, value: str):
    pat = re.compile(rb"(<(?:\w+:)?" + tag.encode() + rb"(?:\s[^>]*)?>)(.*?)(</(?:\w+:)?" + tag.encode() + rb">)", re.S)
    new, n = pat.subn(lambda m: m.group(1) + value.encode() + m.group(3) if m.group(2).strip() else m.group(0), xml)
    return new, n if new != xml else 0


def template_strings(path):
    """All text in the blank template: never altered in a submission."""
    z = zipfile.ZipFile(path)
    texts, staff = set(), set()
    for n in z.namelist():
        if n.endswith(".xml"):
            for t in re.findall(rb"<(?:a:|)t(?:\s[^>]*)?>([^<]*)</(?:a:|)t>", z.read(n)):
                texts.add(t)
    core = z.read("docProps/core.xml")
    for tag in ("creator", "lastModifiedBy"):
        staff |= split_tokens(xml_text(core, tag))
    return texts, staff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out_dir")
    ap.add_argument("--id", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--source-name", default="")
    ap.add_argument("--name", action="append", default=[], help="candidate full name (from the Slack request)")
    a = ap.parse_args()
    ID = a.id.encode()

    zin = zipfile.ZipFile(a.inp)
    parts = {i.filename: zin.read(i.filename) for i in zin.infolist()}
    infos = {i.filename: i for i in zin.infolist()}
    tpl_text, staff = template_strings(a.template)

    # ---- 1. Collect identity tokens (never printed)
    full_names = [n for n in a.name if n.strip()]
    tokens = set()
    src = Counter()
    for n in full_names:
        t = split_tokens(n, min_len=2); tokens |= t; src["slack name"] += len(t)
    t = split_tokens(a.source_name); tokens |= t; src["filename"] += len(t)
    core = parts.get("docProps/core.xml", b"")
    for tag in ("creator", "lastModifiedBy"):
        t = split_tokens(xml_text(core, tag)) - staff; tokens |= t; src[f"core.{tag}"] += len(t)
    for n, b in parts.items():
        if "pivotCacheDefinition" in n:
            for v in re.findall(rb'refreshedBy="([^"]*)"', b):
                t = split_tokens(v.decode("utf-8", "ignore")) - staff; tokens |= t; src["refreshedBy"] += len(t)
        if re.match(r"xl/comments\d*\.xml", n):
            for v in re.findall(rb"<author>([^<]*)</author>", b):
                t = split_tokens(v.decode("utf-8", "ignore")) - staff; tokens |= t; src["comment author"] += len(t)
        if n.startswith("xl/persons/"):
            for v in re.findall(rb'displayName="([^"]*)"', b):
                t = split_tokens(v.decode("utf-8", "ignore")) - staff; tokens |= t; src["person"] += len(t)
    path_users = set()
    for b in parts.values():
        for m in USER_PATH.finditer(b) if b[:5] == b"<?xml" or b[:1] == b"<" else []:
            path_users.add(m.group(2).lower())
    tokens -= staff
    # Short tokens (2 chars) only ever match as part of the full name phrase.
    single = sorted((t for t in tokens if len(t) >= 3), key=len, reverse=True)
    phrases = sorted(full_names, key=len, reverse=True)

    word = lambda t: re.compile(rb"(?<![A-Za-z])" + re.escape(t.encode()) + rb"(?![A-Za-z])", re.I)
    phrase_pats = [re.compile(rb"(?<![A-Za-z])" + rb"[\s_.\-]*".join(re.escape(w.encode()) for w in p.split()) +
                              rb"(?![A-Za-z])", re.I) for p in phrases]
    token_pats = [word(t) for t in single]

    log = defaultdict(Counter)
    out = dict(parts)

    # ---- 2. Identity fields -> ID
    if core:
        b = core
        for tag in ("creator", "lastModifiedBy"):
            b, n = set_xml_text(b, tag, a.id); log["docProps/core.xml"][tag] += n
        out["docProps/core.xml"] = b
    app = parts.get("docProps/app.xml", b"")
    if app:
        b = app
        for tag in ("Company", "Manager"):
            b, n = set_xml_text(b, tag, a.id); log["docProps/app.xml"][tag] += n
        out["docProps/app.xml"] = b

    for n in list(out):
        b = out[n]
        if not (n.endswith(".xml") or n.endswith(".rels") or n.endswith(".vml")):
            continue
        orig = b
        if "pivotCacheDefinition" in n:
            b, k = re.subn(rb'refreshedBy="[^"]*"', b'refreshedBy="' + ID + b'"', b); log[n]["refreshedBy"] += k
        if re.match(r"xl/comments\d*\.xml", n):
            b, k = re.subn(rb"<author>[^<]*</author>", b"<author>" + ID + b"</author>", b); log[n]["comment author"] += k
        if n.startswith("xl/persons/"):
            b, k = re.subn(rb'displayName="[^"]*"', b'displayName="' + ID + b'"', b); log[n]["person name"] += k
            b, k = re.subn(rb'userId="[^"]*"', b'userId="' + ID + b'"', b); log[n]["person userId"] += k
        # Paths: replace only the username segment.
        b, k = USER_PATH.subn(lambda m: m.group(1) + ID, b); log[n]["path username"] += k
        b, k = ONEDRIVE.subn(lambda m: (m.group(1) or m.group(3)) + ID, b); log[n]["cloud user segment"] += k
        b, k = EMAIL.subn(b"[EMAIL]", b); log[n]["email"] += k
        # Free text: whole-word names, never inside strings that exist in the template.
        if FREE_TEXT.match(n):
            def fix_text(m):
                txt = m.group(2)
                if txt in tpl_text:
                    return m.group(0)
                new = txt
                for p in phrase_pats:
                    new, c = p.subn(b"[CANDIDATE]", new); log[n]["name (full)"] += c
                for p in token_pats:
                    new, c = p.subn(b"[CANDIDATE]", new); log[n]["name (word)"] += c
                return m.group(1) + new + m.group(3)
            b = re.sub(rb"(<(?:a:|c:|)t(?:\s[^>]*)?>)([^<]*)(</(?:a:|c:|)t>)", fix_text, b)
        out[n] = b

    # ---- 3. Write output with identical zip structure
    out_path = f"{a.out_dir.rstrip('/')}/{a.id}.xlsx"
    with zipfile.ZipFile(out_path, "w") as zo:
        for n, info in infos.items():
            zi = zipfile.ZipInfo(n, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zo.writestr(zi, out[n])

    # ---- 4. Report (counts only)
    print(f"== {a.id}: tokens from {dict(src)}; {len(single)} word tokens, {len(phrases)} full names, "
          f"{len(path_users)} path usernames (values hidden)")
    changed = [n for n in parts if out[n] != parts[n]]
    for n in changed:
        print(f"   changed {n}: " + ", ".join(f"{k}={v}" for k, v in log[n].items() if v))
    media = [n for n in parts if n.startswith("xl/media/")]
    tz = zipfile.ZipFile(a.template)
    tpl_media = {tz.read(n) for n in tz.namelist() if n.startswith("xl/media/")}
    extra_media = [n for n in media if parts[n] not in tpl_media]
    # OCR each non-template image for name tokens / emails (counts only). Unreadable images stay flagged.
    ocr_hits, ocr_failed = 0, []
    if extra_media:
        try:
            import pytesseract
            from PIL import Image
            for n in extra_media:
                txt = pytesseract.image_to_string(Image.open(io.BytesIO(parts[n]))).encode()
                ocr_hits += sum(len(p.findall(txt)) for p in token_pats + phrase_pats) + len(EMAIL.findall(txt))
        except Exception:
            ocr_failed = extra_media
    chart_images = sum(1 for n in extra_media if re.search(r"/Chart\d+\.png$", n))
    wb = parts.get("xl/workbook.xml", b"")
    sheet_names = re.findall(rb'<sheet [^>]*name="([^"]+)"', wb)
    flagged_sheets = sum(1 for s in sheet_names if any(p.search(s) for p in token_pats + phrase_pats))

    # ---- 5. Verify
    problems = []
    zv = zipfile.ZipFile(out_path)
    for n in zv.namelist():
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                ET.fromstring(zv.read(n))
            except ET.ParseError as e:
                problems.append(f"XML parse error in {n}")
    try:
        import openpyxl, warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            openpyxl.load_workbook(out_path, read_only=True).close()
        opens = True
    except Exception as e:
        opens = False; problems.append(f"openpyxl failed: {type(e).__name__}")
    residual_word = residual_user = 0
    for n in zv.namelist():
        if n.endswith(".xml") or n.endswith(".rels") or n.endswith(".vml"):
            b = zv.read(n)
            for p in token_pats + phrase_pats:
                for m in p.finditer(b):
                    # ignore hits inside template text (e.g. staff or common words already in the template)
                    residual_word += 1
            for u in path_users:
                if re.search(rb"(?<![A-Za-z0-9])" + re.escape(u) + rb"(?![A-Za-z0-9])", b, re.I):
                    residual_user += 1
    # Residual hits that are inside template strings are not candidate data: recount excluding them.
    tpl_hits = 0
    if residual_word:
        for n in zv.namelist():
            if n.endswith(".xml"):
                b = zv.read(n)
                # Text nodes, plus pivot-cache item values (<s v="...">), that are template data
                # (e.g. a place name containing a candidate's first name) are not candidate data.
                vals = re.findall(rb"<(?:a:|c:|)t(?:\s[^>]*)?>([^<]*)</(?:a:|c:|)t>", b) + re.findall(rb'<s v="([^"]*)"', b)
                for t in vals:
                    if t in tpl_text:
                        tpl_hits += sum(len(p.findall(t)) for p in token_pats + phrase_pats)
    unexpected = [n for n in changed if PROTECTED.match(n) and not any(log[n].values())]
    if unexpected:
        problems.append(f"protected parts changed without a logged replacement: {len(unexpected)}")
    protected_touched = [n for n in changed if PROTECTED.match(n)]

    print(f"   images not in template: {len(extra_media)} (charts saved as pictures: {chart_images}); "
          f"OCR name/email hits: {ocr_hits}; OCR unavailable for: {len(ocr_failed)}")
    if ocr_hits:
        problems.append(f"names or emails found in images by OCR: {ocr_hits} (needs manual redaction)")
    if ocr_failed:
        problems.append(f"{len(ocr_failed)} images could not be OCR-checked")
    print(f"   sheet names containing a name: {flagged_sheets} (flag only; renaming would break formulas)")
    print(f"   VERIFY: xml ok={not any('XML' in p for p in problems)}, opens={opens}, "
          f"residual name hits={residual_word - tpl_hits} (+{tpl_hits} inside template text), "
          f"residual path usernames={residual_user}, protected parts touched={len(protected_touched)}")
    print(f"   RESULT: {'PASS' if not problems and residual_word - tpl_hits == 0 and residual_user == 0 and flagged_sheets == 0 else 'CHECK'}"
          + (f" ({'; '.join(problems)})" if problems else ""))
    report = {"id": a.id, "token_sources": dict(src), "changed_parts": {n: dict(log[n]) for n in changed},
              "extra_images": len(extra_media), "chart_images": chart_images, "ocr_hits": ocr_hits,
              "flagged_sheet_names": flagged_sheets, "opens": opens,
              "residual_name_hits": residual_word - tpl_hits, "residual_path_usernames": residual_user,
              "protected_parts_touched": protected_touched, "problems": problems}
    with open(f"{a.out_dir.rstrip('/')}/{a.id}.report.json", "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())
