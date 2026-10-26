import csv
from pathlib import Path

from render.chpfill import load_vocabulary
from tools.odp_tables import defaults_text, key, vocab_block

TOP = Path(__file__).resolve().parents[1]
ROWS = list(csv.DictReader(open(TOP / "rev3/odp-values.csv", encoding="utf-8")))
CAT = {r["id"] for r in csv.DictReader(open(TOP / "rev3/catalog.csv", encoding="utf-8"))}


def test_eighty_odps_over_fifty_requirements_four_guidance():
    ids = [r["odp_id"] for r in ROWS]
    assert len(ids) == 80 and len(set(ids)) == 80
    assert len({r["requirement_id"] for r in ROWS}) == 50
    assert sum(r["kind"] == "guidance" for r in ROWS) == 4 and {r["kind"] for r in ROWS} == {"value", "guidance"}
    for r in ROWS:
        assert r["requirement_id"] == r["odp_id"][:8] and r["requirement_id"] in CAT
        assert r["assignment"].startswith(("[Assignment:", "[Selection")) and r["assignment"].endswith("]")
        assert r["value"].strip() and "significant1" not in r["value"]


def test_key_form():
    assert key("03.01.01.f.02") == "odp.03_01_01_f_02" and key("03.04.06.b") == "odp.03_04_06_b"


def test_defaults_file_is_generated_from_the_values():
    assert (TOP / "rev3/defaults.ini").read_text() == defaults_text(ROWS)
    text = defaults_text(ROWS)
    assert "\n[odp]\n" in text and "03_01_01_f_02 = at most 90 days\n" in text
    assert sum(1 for ln in text.split("\n") if " = " in ln and not ln.startswith("#")) == 76


def test_vocabulary_has_every_odp_once_as_public():
    voc = (TOP / "vocabulary.md").read_text()
    assert vocab_block(ROWS) in voc
    v = load_vocabulary(TOP / "vocabulary.md")
    for r in ROWS:
        assert v[key(r["odp_id"])]["visibility"] == "public" and v[key(r["odp_id"])]["kind"] == "value"


def test_no_line_wrap_hyphen_artefacts():
    # final review M1: "non- remote", "800- 47", "end- point" were pdftotext line-wrap artefacts
    import re
    assert [r["odp_id"] for r in ROWS if re.search(r"[A-Za-z0-9]- [A-Za-z0-9]", r["value"])] == []
