import re
from pathlib import Path

from render.chpfill import load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]
POAM = (TOP / "rev2/templates/poam/frame.md").read_text()
IDS = [f"T-{n:02d}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)]


def _rows():
    return [[c.strip() for c in ln.strip("|").split("|")] for ln in POAM.split("\n") if ln.startswith("| T-")]


def test_seed_ids_are_complete_and_in_order():
    assert [r[0] for r in _rows()] == IDS


def test_every_seed_has_eight_cells_a_date_placeholder_and_open_status():
    for r in _rows():
        assert len(r) == 8, r[0]
        assert r[1] == "Rev 2" and r[7] == "Open", r[0]
        assert r[5] == "{{poam.due_t%s}}" % r[0][2:], r[0]
        assert r[6] in ("{{roles.security_officer}}", "{{roles.administrator}}"), r[0]
        assert "Seeded by the template: confirm, adapt or close." in r[3], r[0]


def test_every_due_key_is_in_the_vocabulary_as_private():
    v = load_vocabulary(TOP / "vocabulary.md")
    for i in IDS:
        assert vocab_entry("poam.due_t" + i[2:], v), i
    text = (TOP / "vocabulary.md").read_text()
    for i in IDS[7:]:
        assert ("| `poam.due_t%s` | value | private |" % i[2:]) in text


def test_document_server_requirement_numbers_are_owner_confirmed_and_unflagged():  # confirmed by the owner 2026-11-27
    assert "PENDING OWNER CONFIRMATION" not in POAM
    for r in _rows()[7:]:
        assert re.fullmatch(r"3\.\d+\.\d+(, 3\.\d+\.\d+)*", r[2]), r[0]


def test_new_seeds_carry_no_site_values():
    new = "\n".join(ln for ln in POAM.split("\n") if re.match(r"\| T-(0[89]|1[0-6]) ", ln))
    assert not re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b|@|\.(net|org|com|local|lan)\b", new)
