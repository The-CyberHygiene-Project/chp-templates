import csv
import re
from pathlib import Path

import pytest
from render.chpfill import TOKEN, load_vocabulary, vocab_entry
from tools.gen_rev3_blocks import block_text, main, rev2_basis
from tools.odp_tables import key

TOP = Path(__file__).resolve().parents[1]
CTRL = TOP / "rev3/templates/ssp/controls"
HEAD = re.compile(r"^<!-- chp:control id=(\S+) status=(appliance|site|partial|pending) evidence=(\S*) -->\n")
IDS = [r["id"] for r in csv.DictReader(open(TOP / "rev3/catalog.csv", encoding="utf-8"))]
XW = list(csv.DictReader(open(TOP / "rev3/crosswalk.csv", encoding="utf-8")))
ODP = list(csv.DictReader(open(TOP / "rev3/odp-values.csv", encoding="utf-8")))


def test_one_block_per_rev3_requirement():
    assert sorted(p.stem for p in CTRL.glob("*.md")) == sorted(IDS)


@pytest.mark.parametrize("cid", IDS)
def test_block_header_odps_and_vocabulary(cid):
    text = (CTRL / f"{cid}.md").read_text()
    m = HEAD.match(text)
    assert m and m.group(1) == cid
    if m.group(2) in ("appliance", "partial"):
        assert m.group(3), "appliance/partial must cite evidence"
    if m.group(2) == "pending":
        assert m.group(3) == "" and "not yet proven" in text and "**Site responsibility:** " in text
    used = {t.group(1) for t in TOKEN.finditer(text) if t.group(1).startswith("odp.")}
    assert used == {key(r["odp_id"]) for r in ODP if r["requirement_id"] == cid}
    v = load_vocabulary(TOP / "vocabulary.md")
    assert all(vocab_entry(t.group(1), v) for t in TOKEN.finditer(text))


def test_guidance_odps_quote_dod_guidance():
    for r in (r for r in ODP if r["kind"] == "guidance"):
        text = (CTRL / f"{r['requirement_id']}.md").read_text()
        line = next(ln for ln in text.split("\n") if f"{{{{{key(r['odp_id'])}}}}}" in ln)
        assert "*DoD gives guidance, not a value: " in line


def test_rev2_basis_lines_follow_the_crosswalk():
    basis = rev2_basis(XW)
    assert basis["03.01.12"] == (["3.1.12"], ["3.1.13", "3.1.14", "3.1.15", "3.13.7"])   # 3.13.7: "Addressed by 03.01.12, ..."
    assert basis["03.15.02"][0] == ["3.12.4"]
    assert "3.11.4" not in str(basis)
    assert basis.get("03.04.10", ([], [])) == ([], [])                  # new in Rev 3
    assert "**Rev 2 basis:** none; this requirement is new in Rev 3." in (CTRL / "03.04.10.md").read_text()
    assert "**Rev 2 basis:** 3.1.1; it also covers withdrawn 3.13.3. " in (CTRL / "03.01.01.md").read_text()
    assert "**Rev 2 basis:** 3.12.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.12.4." in \
        (CTRL / "03.15.02.md").read_text()
    assert not [p.stem for p in CTRL.glob("*.md") if "appliance" in p.read_text()]   # final review I4


def test_block_text_exact_form():
    t = block_text("03.09.09", ([], []), [])
    assert t == ("<!-- chp:control id=03.09.09 status=pending evidence= -->\n"
                 "**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, "
                 "so this library does not yet describe an implementation.\n\n"
                 "**Rev 2 basis:** none; this requirement is new in Rev 3.\n\n"
                 "**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text "
                 "is written.\n")


def test_generator_never_overwrites_a_block(tmp_path, monkeypatch):
    import tools.gen_rev3_blocks as g
    monkeypatch.setattr(g, "CTRL", tmp_path)
    (tmp_path / "03.01.01.md").write_text("hand edited\n")
    main()
    assert (tmp_path / "03.01.01.md").read_text() == "hand edited\n"
    assert len(list(tmp_path.glob("*.md"))) == 97
