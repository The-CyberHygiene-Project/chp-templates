import csv
import re
from pathlib import Path

from render.chpfill import TOKEN, load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]
FRAME = (TOP / "rev3/templates/ssp/frame.md").read_text()
POAM = (TOP / "rev3/templates/poam/frame.md").read_text()
XW = {r["rev2_id"]: r["rev3_ids"].split() for r in csv.DictReader(open(TOP / "rev3/crosswalk.csv"))}
ORDER = ["## DOCUMENT CONTROL", "## EXECUTIVE SUMMARY", "## 2. SYSTEM IDENTIFICATION", "## 3. SYSTEM DESCRIPTION",
         "## 4. SECURITY CONTROL IMPLEMENTATION", "## 5. CONTINGENCY PLANNING (CP)", "## 6. SECURITY POLICIES AND PROCEDURES",
         "## 10. PLAN OF ACTION AND MILESTONES (POA&M)", "## 11. IMPLEMENTATION METRICS", "## 12. CONCLUSION",
         "## AUTHORIZATION", "## APPENDICES"]


def test_same_fixed_layouts_as_rev2():
    pos = [FRAME.index(h + "\n") for h in ORDER]
    assert pos == sorted(pos)
    assert "| Version | Date | Author | Description |\n|:---|:---|:---|:---|\n" in FRAME
    assert "{{assessment.sprs_score}}" in FRAME and "| **Strict 800-171A objectives met** |" in FRAME
    assert "**{{assessment.objectives_met}}/97**" in FRAME
    for inc in ("{{> arch}}", "{{> controls}}", "{{> family_status}}"):
        assert FRAME.count(inc) == 1
    assert FRAME.rstrip().endswith("*Add further lettered appendices below; nothing reads their order.*")


def test_frame_is_rev3_and_explains_pending_and_odps():
    assert "## NIST SP 800-171 Rev 3 Compliance" in FRAME and "/110" not in FRAME
    assert "- **pending:**" in FRAME and "April 10, 2025" in FRAME
    assert len(re.findall(r"Rev 2", FRAME)) == len(re.findall(r"Rev 2 basis|CMMC Level 2 assessments use Rev 2", FRAME))


def test_every_placeholder_is_in_the_vocabulary():
    v = load_vocabulary(TOP / "vocabulary.md")
    for text in (FRAME, POAM, (TOP / "rev3/templates/ssp/arch/chp-appliance.md").read_text()):
        assert all(vocab_entry(m.group(1), v) for m in TOKEN.finditer(text))


def test_poam_seeds_use_the_crosswalk():
    rows = [ln for ln in POAM.split("\n") if ln.startswith("| T-")]
    assert [r.split(" | ")[0] for r in rows] == ["| T-01", "| T-02", "| T-03", "| T-04", "| T-05", "| T-07"]
    seeds = {"T-01": ["3.10.4"], "T-02": ["3.13.11", "3.5.10"], "T-03": ["3.8.6"],
             "T-04": ["3.1.10", "3.1.11", "3.13.9"], "T-05": ["3.5.6", "3.5.8"], "T-07": ["3.4.3"]}
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        assert cells[1] == "Rev 3"
        want = sorted({t for r2 in seeds[cells[0]] for t in XW[r2]})
        if cells[0] == "T-05":       # 3.5.6/3.5.8 withdrawn with no successor; inactivity now lives in 03.01.01.f.02
            assert want == [] and "{{odp.03_01_01_f_02}}" in r
            want = ["03.01.01"]
        assert cells[2] == ", ".join(want), cells[0]
    assert "T-06" in POAM and "0.2.0-update3" in POAM


def test_rev2_t06_says_closed_by_update3():
    t06 = next(ln for ln in (TOP / "rev2/templates/poam/frame.md").read_text().split("\n") if ln.startswith("| T-06"))
    assert "0.2.0-update3" in t06 and "still denied" in t06
