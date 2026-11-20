# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""make_doc_templates.py [OUTDIR]: write the controlled-document templates (default: doc/ beside tools/).

  OUTDIR/cui/CUI_Template_v0.1-DRAFT.{docx,xlsx,md}   marked for the CUI area
  OUTDIR/noncui/Template_v0.1-DRAFT.{docx,xlsx,md}    the non-CUI twins: no CUI banner, no designation block

The CUI templates carry the CUI banner and the designation block by construction, in the forms the appliance's
marking checker reads (`chp-site doc check`):
  - docx: a `CUI` paragraph in the default and the first-page header and footer (Header and Footer styles; the section
    has a title page), and the designation block in the first-page footer, above its banner;
  - xlsx: `CUI` in the sheet's header and footer (centre section), and the designation block in cells A1-A3 (a
    header/footer is limited to 255 characters, too short for three values of up to 128 each);
  - md: `CUI` as the first and the last line, and the designation block after the first one.
The block lines are `Controlled by: {{CUI_CONTROLLED_BY}}`, `CUI Category: {{CUI_CATEGORY}}` and `POC: {{CUI_POC}}`.
`chp-site doc new` fills the three placeholders from the site keys of the same names (never typed per file).

Standard library only, Python 3.9. Byte-reproducible: fixed member order, fixed dates, stored (uncompressed) members,
so the output does not depend on the zlib version. Re-run after a change and commit the result; a test compares."""
import io
import sys
import zipfile
from pathlib import Path

DATE = (1980, 1, 1, 0, 0, 0)
XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
OD = R + "/"
OX = "application/vnd.openxmlformats-officedocument."
BANNER = "CUI"
BLOCK = ["Controlled by: {{CUI_CONTROLLED_BY}}", "CUI Category: {{CUI_CATEGORY}}", "POC: {{CUI_POC}}"]
TITLE = "Title"
SECTIONS = [("Purpose", "State what this document is for and which requirements it supports."),
            ("Scope", "State the systems, people and information it covers."),
            ("Content", "Write the document here.")]
NOTE = "Versions and approvals are recorded by the document workflow; do not type them here."


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def package(members):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for name, data in members:
            zi = zipfile.ZipInfo(name, DATE)
            zi.compress_type = zipfile.ZIP_STORED
            zi.create_system = 3
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data.encode("utf-8"))
    return b.getvalue()


def rels(items):
    return (f'{XML}<Relationships xmlns="{PR}">'
            + "".join(f'<Relationship Id="{i}" Type="{OD}{t}" Target="{g}"/>' for i, t, g in items)
            + "</Relationships>")


def types(overrides):
    return (f'{XML}<Types xmlns="{CT}">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            + "".join(f'<Override PartName="{p}" ContentType="{c}"/>' for p, c in overrides) + "</Types>")


# ---------- docx ----------

def para(text, style=None, center=False):
    ppr = ""
    if style or center:
        ppr = ("<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "")
               + ('<w:jc w:val="center"/>' if center else "") + "</w:pPr>")
    return f'<w:p>{ppr}<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'


def hf(kind, paras):
    tag = "hdr" if kind == "header" else "ftr"
    return f'{XML}<w:{tag} xmlns:w="{W}">{"".join(paras)}</w:{tag}>'


STYLES_DOCX = (
    f'{XML}<w:styles xmlns:w="{W}">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="22"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240"/><w:outlineLvl w:val="0"/>'
    '</w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>'
    "</w:styles>")


def docx(cui):
    body = [para(TITLE, "Title")]
    for head, text in SECTIONS:
        body += [para(head, "Heading1"), para(text)]
    body.append(para(NOTE))
    banner_h, banner_f = para(BANNER, "Header", True), para(BANNER, "Footer", True)
    if cui:
        parts = [("header1.xml", "header", [banner_h]), ("header2.xml", "header", [banner_h]),
                 ("footer1.xml", "footer", [banner_f]),
                 ("footer2.xml", "footer", [para(x, "Footer") for x in BLOCK] + [banner_f])]
        refs = [("header", "default", "rId4"), ("header", "first", "rId5"), ("footer", "default", "rId6"),
                ("footer", "first", "rId7")]
    else:
        parts = [("header1.xml", "header", [para("", "Header")]), ("footer1.xml", "footer", [para("", "Footer")])]
        refs = [("header", "default", "rId4"), ("footer", "default", "rId5")]
    sect = ("<w:sectPr>"
            + "".join(f'<w:{k}Reference w:type="{t}" r:id="{i}"/>' for k, t, i in refs)
            + '<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
            'w:header="720" w:footer="720" w:gutter="0"/>' + ("<w:titlePg/>" if cui else "") + "</w:sectPr>")
    document = f'{XML}<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{"".join(body)}{sect}</w:body></w:document>'
    doc_rels = [("rId1", "styles", "styles.xml"), ("rId2", "settings", "settings.xml")]
    doc_rels += [(i, k, f) for (f, k, _), (_, _, i) in zip(parts, refs)]
    overrides = [("/word/document.xml", OX + "wordprocessingml.document.main+xml"),
                 ("/word/styles.xml", OX + "wordprocessingml.styles+xml"),
                 ("/word/settings.xml", OX + "wordprocessingml.settings+xml")]
    overrides += [(f"/word/{f}", OX + f"wordprocessingml.{k}+xml") for f, k, _ in parts]
    members = [("[Content_Types].xml", types(overrides)),
               ("_rels/.rels", rels([("rId1", "officeDocument", "word/document.xml")])),
               ("word/document.xml", document),
               ("word/_rels/document.xml.rels", rels(doc_rels)),
               ("word/styles.xml", STYLES_DOCX),
               ("word/settings.xml", f'{XML}<w:settings xmlns:w="{W}"/>')]
    members += [(f"word/{f}", hf(k, ps)) for f, k, ps in parts]
    return package(members)


# ---------- xlsx ----------

STYLES_XLSX = (
    f'{XML}<styleSheet xmlns="{S}">'
    '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
    '<font><b/><sz val="14"/><name val="Calibri"/></font></fonts>'
    '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
    '</fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
    '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
    '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
    '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
    '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
    "</styleSheet>")


def cell(ref, text, style=0):
    s = f' s="{style}"' if style else ""
    return f'<c r="{ref}"{s} t="inlineStr"><is><t xml:space="preserve">{esc(text)}</t></is></c>'


def xlsx(cui):
    rows = [(i + 1, [cell(f"A{i + 1}", x)]) for i, x in enumerate(BLOCK)] if cui else []
    top = len(rows) + 2 if cui else 1
    rows.append((top, [cell(f"A{top}", TITLE, 1)]))
    rows.append((top + 1, [cell(f"A{top + 1}", NOTE)]))
    data = "".join(f'<row r="{n}">{"".join(cs)}</row>' for n, cs in rows)
    hfx = (f"<headerFooter><oddHeader>{esc('&C' + BANNER)}</oddHeader><oddFooter>{esc('&C' + BANNER)}</oddFooter>"
           "</headerFooter>") if cui else ""
    sheet = (f'{XML}<worksheet xmlns="{S}"><dimension ref="A1:A{top + 1}"/><sheetViews><sheetView workbookViewId="0"/>'
             f'</sheetViews><sheetFormatPr defaultRowHeight="15"/><cols><col min="1" max="1" width="80" '
             f'customWidth="1"/></cols><sheetData>{data}</sheetData><pageMargins left="0.7" right="0.7" top="0.75" '
             f'bottom="0.75" header="0.3" footer="0.3"/>{hfx}</worksheet>')
    wb = (f'{XML}<workbook xmlns="{S}" xmlns:r="{R}"><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>'
          "</workbook>")
    overrides = [("/xl/workbook.xml", OX + "spreadsheetml.sheet.main+xml"),
                 ("/xl/worksheets/sheet1.xml", OX + "spreadsheetml.worksheet+xml"),
                 ("/xl/styles.xml", OX + "spreadsheetml.styles+xml")]
    return package([("[Content_Types].xml", types(overrides)),
                    ("_rels/.rels", rels([("rId1", "officeDocument", "xl/workbook.xml")])),
                    ("xl/workbook.xml", wb),
                    ("xl/_rels/workbook.xml.rels", rels([("rId1", "worksheet", "worksheets/sheet1.xml"),
                                                         ("rId2", "styles", "styles.xml")])),
                    ("xl/worksheets/sheet1.xml", sheet),
                    ("xl/styles.xml", STYLES_XLSX)])


# ---------- md ----------

def md(cui):
    body = [f"# {TITLE}", ""]
    for head, text in SECTIONS:
        body += [f"## {head}", "", text, ""]
    body += [NOTE]
    if cui:
        lines = [BANNER, ""] + [x for b in BLOCK for x in (b, "")] + body + ["", BANNER]
    else:
        lines = body
    return ("\n".join(lines) + "\n").encode("utf-8")


MAKERS = {"docx": docx, "xlsx": xlsx, "md": md}


def main(argv):
    out = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "doc"
    for area, prefix, cui in (("cui", "CUI_", True), ("noncui", "", False)):
        (out / area).mkdir(parents=True, exist_ok=True)
        for ext, make in MAKERS.items():
            (out / area / f"{prefix}Template_v0.1-DRAFT.{ext}").write_bytes(make(cui))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
