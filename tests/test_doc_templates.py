"""The controlled-document templates in doc/ (1.4.0): made by tools/make_doc_templates.py (stdlib, byte-reproducible),
placeholders only. `chp-site doc new` (idm-assistant) fills {{CUI_CONTROLLED_BY}}, {{CUI_CATEGORY}} and {{CUI_POC}}
from the site keys; idm-assistant's test_templates_pass_checker_after_fill runs its marking checker on the result."""
import csv
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import pytest
from render.chpfill import load_vocabulary

TOP = Path(__file__).resolve().parents[1]
DOC = TOP / "doc"
PH = ("{{CUI_CONTROLLED_BY}}", "{{CUI_CATEGORY}}", "{{CUI_POC}}")
BLOCK = ["Controlled by: {{CUI_CONTROLLED_BY}}", "CUI Category: {{CUI_CATEGORY}}", "POC: {{CUI_POC}}"]
NAMES = {"cui": ["CUI_Template_v0.1-DRAFT.docx", "CUI_Template_v0.1-DRAFT.md", "CUI_Template_v0.1-DRAFT.xlsx"],
         "fci": ["FCI_Template_v0.1-DRAFT.docx", "FCI_Template_v0.1-DRAFT.md", "FCI_Template_v0.1-DRAFT.xlsx"],
         "noncui": ["Template_v0.1-DRAFT.docx", "Template_v0.1-DRAFT.md", "Template_v0.1-DRAFT.xlsx"]}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NEW_KEYS = {"DOC_ISSO_ACCOUNT": ("roles.doc_isso_account", "private"),
            "DOC_APPROVER_ACCOUNTS": ("roles.doc_approver_accounts", "private"),
            "CUI_CONTROLLED_BY": ("marking.controlled_by", "public"),
            "CUI_CATEGORY": ("marking.cui_category", "public"),
            "CUI_POC": ("marking.poc", "private")}


def make(out):
    r = subprocess.run([sys.executable, "-I", str(TOP / "tools/make_doc_templates.py"), str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return out


def test_committed_templates_are_exactly_what_the_tool_makes(tmp_path):
    out = make(tmp_path / "a")
    made = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    have = sorted(p.relative_to(DOC).as_posix() for p in DOC.rglob("*") if p.is_file())
    assert made == have == sorted(f"{a}/{n}" for a, ns in NAMES.items() for n in ns)
    for rel in made:
        assert (out / rel).read_bytes() == (DOC / rel).read_bytes(), f"{rel}: re-run tools/make_doc_templates.py"


def test_the_tool_is_byte_reproducible(tmp_path):
    a, b = make(tmp_path / "a"), make(tmp_path / "b")
    for rel in (f"{x}/{n}" for x, ns in NAMES.items() for n in ns):
        assert (a / rel).read_bytes() == (b / rel).read_bytes(), rel


def test_committed_so_the_docx_ignore_rule_does_not_drop_them():
    out = subprocess.run(["git", "ls-files", "doc"], cwd=TOP, capture_output=True, text=True).stdout.split()
    assert sorted(out) == sorted(f"doc/{a}/{n}" for a, ns in NAMES.items() for n in ns)


def _zip(p):
    z = zipfile.ZipFile(p)
    assert all(i.compress_type == zipfile.ZIP_STORED and i.date_time == (1980, 1, 1, 0, 0, 0) for i in z.infolist())
    return z


def _lines(root):
    return ["".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p")]


def _docx_parts(z):
    doc = ET.fromstring(z.read("word/document.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
    sect = doc.find(f"{W}body/{W}sectPr")
    refs = {(e.tag[len(W):], e.get(W + "type")): ET.fromstring(z.read("word/" + rels[e.get(R + "id")]))
            for e in sect if e.tag in (W + "headerReference", W + "footerReference")}
    return doc, sect, refs


def test_cui_docx_banner_every_page_and_block_in_the_first_page_footer():
    z = _zip(DOC / "cui" / NAMES["cui"][0])
    doc, sect, refs = _docx_parts(z)
    assert sect.find(W + "titlePg") is not None
    assert set(refs) == {(k, t) for k in ("headerReference", "footerReference") for t in ("default", "first")}
    for key, root in refs.items():
        assert "CUI" in _lines(root), key
    first_footer = _lines(refs[("footerReference", "first")])
    assert first_footer == BLOCK + ["CUI"]                     # the designation block on page one, then the banner
    assert "Header" in z.read("word/styles.xml").decode() and "Footer" in z.read("word/styles.xml").decode()
    assert not any("CUI" == x for x in _lines(doc))             # the body is the author's; marks are header/footer


def test_cui_xlsx_banner_in_header_and_footer_and_block_in_rows_1_to_3():
    z = _zip(DOC / "cui" / NAMES["cui"][2])
    sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    hf = sheet.find(S + "headerFooter")
    assert hf.findtext(S + "oddHeader") == "&CCUI" and hf.findtext(S + "oddFooter") == "&CCUI"
    assert hf.get("differentFirst") is None and hf.get("differentOddEven") is None
    cells = {c.get("r"): "".join(t.text or "" for t in c.iter(S + "t")) for c in sheet.iter(S + "c")}
    assert [cells["A1"], cells["A2"], cells["A3"]] == BLOCK


def test_cui_md_banner_first_and_last_and_block_after_the_first_banner():
    lines = (DOC / "cui" / NAMES["cui"][1]).read_text(encoding="utf-8").splitlines()
    assert lines[0] == "CUI" and lines[-1] == "CUI"
    assert [x for x in lines[1:7] if x] == BLOCK


@pytest.mark.parametrize("name", NAMES["cui"])
def test_each_cui_placeholder_appears_once(name):
    p = DOC / "cui" / name
    text = (b"".join(_zip(p).read(n) for n in _zip(p).namelist()) if p.suffix != ".md" else p.read_bytes()).decode()
    assert [text.count(x) for x in PH] == [1, 1, 1]
    assert set(re.findall(r"\{\{[^}]*\}\}", text)) == set(PH)


@pytest.mark.parametrize("name", NAMES["noncui"])
def test_noncui_twins_have_no_cui_banner_and_no_placeholders(name):
    p = DOC / "noncui" / name
    if p.suffix == ".md":
        texts = p.read_text(encoding="utf-8").splitlines()
    elif p.suffix == ".docx":
        z = _zip(p)
        texts = [x for n in z.namelist() if n.endswith(".xml") and n.startswith("word/")
                 for x in _lines(ET.fromstring(z.read(n)))]
    else:
        z = _zip(p)
        texts = [t.text or "" for n in z.namelist() if n.endswith(".xml") for t in ET.fromstring(z.read(n)).iter()]
    assert not any(re.fullmatch(r"\s*(&C)?CUI(//\S*)?\s*", x or "") for x in texts)
    assert not any("{{" in (x or "") or "CUI" in (x or "") for x in texts)


def test_names_follow_the_name_rule():
    rule = re.compile(r"(CUI_|FCI_)?[A-Za-z0-9][A-Za-z0-9_-]*_v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)-DRAFT\.(docx|xlsx|md)")
    for area, ns in NAMES.items():
        for n in ns:
            assert rule.fullmatch(n) and n.startswith("CUI_") == (area == "cui"), n
            assert n.startswith("FCI_") == (area == "fci"), n


# ---------- FCI (idm-assistant ISO 0.7.0, owner decision 2026-11-20: "FCI should be marked as FCI") ----------

def test_fci_docx_banner_in_every_header_and_footer_and_no_cui_marks():
    z = _zip(DOC / "fci" / NAMES["fci"][0])
    doc, sect, refs = _docx_parts(z)
    assert sect.find(W + "titlePg") is None                     # one header and one footer mark every page
    assert set(refs) == {("headerReference", "default"), ("footerReference", "default")}
    for key, root in refs.items():
        assert _lines(root) == ["FCI"], key
    text = b"".join(z.read(n) for n in z.namelist()).decode()
    assert "{{" not in text and ">CUI<" not in text and "CUI Category" not in text and "Controlled by" not in text


def test_fci_xlsx_banner_in_header_and_footer_and_no_block():
    z = _zip(DOC / "fci" / NAMES["fci"][2])
    sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    hf = sheet.find(S + "headerFooter")
    assert hf.findtext(S + "oddHeader") == "&CFCI" and hf.findtext(S + "oddFooter") == "&CFCI"
    assert hf.get("differentFirst") is None and hf.get("differentOddEven") is None
    text = b"".join(z.read(n) for n in z.namelist()).decode()
    assert "{{" not in text and "CUI" not in text


def test_fci_md_banner_first_and_last_and_no_block():
    text = (DOC / "fci" / NAMES["fci"][1]).read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines[0] == "FCI" and lines[-1] == "FCI"
    assert "{{" not in text and "CUI" not in text


def test_fci_templates_share_the_body_of_the_cui_ones():
    """The same document, other marks: the md body between the marks is the same as the non-CUI twin's."""
    fci = (DOC / "fci" / NAMES["fci"][1]).read_text(encoding="utf-8").splitlines()
    plain = (DOC / "noncui" / NAMES["noncui"][1]).read_text(encoding="utf-8").splitlines()
    assert fci == ["FCI", ""] + plain + ["", "FCI"]


def test_mapping_covers_the_document_keys_and_every_row_is_in_the_vocabulary():
    rows = list(csv.DictReader(open(TOP / "site-conf-mapping.csv", encoding="utf-8")))
    got = {r["site_conf_key"]: (r["placeholder"], r["visibility"]) for r in rows}
    for k, v in NEW_KEYS.items():
        assert got.get(k) == v, k
    vocab = load_vocabulary(TOP / "vocabulary.md")
    for k, (ph, vis) in got.items():
        assert ph in vocab and vocab[ph]["visibility"] == vis, k
    # additive only: the 1.3.x rows are unchanged and first
    assert [r["site_conf_key"] for r in rows[:6]] == ["DOMAIN", "SUBNET", "GATEWAY", "TIMEZONE", "ISSO_NAME",
                                                      "BASELINE_DELEGATES"]


def test_tool_is_stdlib_only():
    src = (TOP / "tools/make_doc_templates.py").read_text()
    mods = {m.split(".")[0] for m in re.findall(r"^\s*(?:import|from)\s+([\w.]+)", src, re.M)}
    assert mods <= {"sys", "zipfile", "io", "pathlib", "os"}, mods


CTRL = TOP / "rev2/templates/ssp/controls"


def _impl(cid):
    return (CTRL / f"{cid}.md").read_text().split("**Site responsibility:**")[0]


def test_document_workflow_narratives_state_the_owner_decisions():
    # ISO 0.7.0 design: decision 2 (download/re-upload), section 12 (MD5 degraded), decision 9 (approval alerts and
    # the forgery residual), the canary and publisher accounts, alert text with CUI file names
    t313, t331, t343 = _impl("3.1.3"), _impl("3.3.1"), _impl("3.4.3")
    assert "download" in t313 and "upload" in t313 and "insider risk" in t313
    assert "MD5" in t313 and "DEGRADED" in t313
    assert "chp-canary" in t313 and "chp-publisher" in t343
    assert "file names" in t331
    assert "every approval and every override" in t343.lower() and "level 12" in t343 and "forge" in t343
    assert "chp-doc" in t343 and "userinfo" in t343
    for cid in ("3.1.3", "3.1.22", "3.3.1", "3.4.3", "3.8.4", "3.8.9", "3.13.8"):
        assert "0.7.0" in _impl(cid), cid
    assert "CUI_CONTROLLED_BY" in _impl("3.8.4") and "marking check" in _impl("3.8.4")


def test_owner_decisions_2026_11_20_fci_marking_and_time_from_the_server():
    t384 = _impl("3.8.4")
    assert "marked FCI" in t384 and "no CUI designation block" in t384 and "FCI banner on a CUI document" in t384
    t337 = _impl("3.3.7")
    assert "takes its time from the server only" in t337 and "never from an outside source" in t337
    # the server tailoring (owner decision 2026-11-20): server tailored out, workstation evidence stands
    assert "on the CHP server the rule is tailored out" in t337 and "on the workstations the scan evidence stands" in t337
    assert "scan:chronyd_client_only" in (CTRL / "3.3.7.md").read_text().splitlines()[0]   # evidence format unchanged
    for cid in ("3.4.7", "3.13.1", "3.13.6"):
        t = _impl(cid)
        assert "123/udp" in t and "site subnet only" in t and "owner-approved exception" in t, cid
    for cid in ("3.3.7", "3.4.7", "3.13.1", "3.13.6", "3.8.4"):      # additive: the 1.4.0 sentences are still there
        assert (CTRL / f"{cid}.md").read_text().count("**Implementation:**") == 1


def test_fix_round_1_alert_hook_and_share_wording():
    t331 = (CTRL / "3.3.1.md").read_text()
    assert "ALERT_HOOK" in _impl("3.3.1") and "are not forwarded off it" not in t331
    assert "CUI boundary or to a channel authorised for CUI" in t331.split("**Site responsibility:**")[1]
    t = _impl("3.1.22")
    assert "every external or federated share" not in t and "federated share" in t and "7 days" in t
