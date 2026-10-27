import csv
from pathlib import Path

import pytest
from tools.import_catalog_r3 import FAMILIES, convert, load

TOP = Path(__file__).resolve().parents[1]
CAT = list(csv.DictReader(open(TOP / "rev3/catalog.csv", encoding="utf-8")))
XW = list(csv.DictReader(open(TOP / "rev3/crosswalk.csv", encoding="utf-8")))
R2 = [r["id"] for r in csv.DictReader(open(TOP / "rev2/catalog.csv", encoding="utf-8"))]


def test_catalog_has_the_97_requirements_in_order():
    ids = [r["id"] for r in CAT]
    assert len(ids) == 97 and len(set(ids)) == 97 and ids == sorted(ids)
    assert list(csv.DictReader(open(TOP / "rev3/catalog.csv")).fieldnames) == ["id", "family", "family_code", "title",
                                                                               "requirement"]


def test_families_come_from_the_id_and_all_17_appear():
    assert len(FAMILIES) == 17
    for r in CAT:
        assert (r["family"], r["family_code"]) == FAMILIES[r["id"][3:5]]
        assert r["title"] and r["title"] != "Withdrawn" and r["requirement"].strip()
        assert "\t" not in r["requirement"] and "\t" not in r["id"]
    assert {r["family_code"] for r in CAT} == {c for _, c in FAMILIES.values()}


def test_crosswalk_covers_exactly_the_rev2_ids():
    assert [r["rev2_id"] for r in XW] == R2


def test_crosswalk_targets_exist_and_changes_are_known():
    ids = {r["id"] for r in CAT}
    for r in XW:
        assert set(r["rev3_ids"].split()) <= ids, r
        assert r["change"] in ("no significant change", "minor change", "significant change", "withdrawn"), r


def test_known_mappings_including_the_nist_erratum():
    x = {r["rev2_id"]: r for r in XW}
    assert x["3.12.4"]["rev3_ids"] == "03.15.02"                       # 3.11.4 row in the workbook is an erratum
    assert x["3.4.7"]["rev3_ids"] == "03.04.06 03.04.08" and x["3.4.7"]["change"] == "withdrawn"
    assert x["3.2.3"]["rev3_ids"] == "03.02.01"                        # NIST text has the typo "03.02 01"
    assert x["3.5.6"]["rev3_ids"] == "" and x["3.5.6"]["note"] == "Consistency with SP 800-53."
    assert (x["3.1.1"]["rev3_ids"], x["3.1.1"]["change"]) == ("03.01.01", "significant change")
    assert x["3.1.1"]["note"].startswith("New security requirement title Aligned with SP 800-53, Rev 5")
    assert all("\n" not in r["note"] for r in XW)


def test_convert_skips_the_erratum_row_and_fixes_spacing():
    head = {"C": "SP 800-171 R2 Identifier", "G": "SP 800-171 R3 Identifier"}
    rows = [head,
            {"C": "3.2.3", "G": "03.02.03", "H": "Withdrawn", "I": "Incorporated into 03.02 01.", "O": "X"},
            {"C": "3.11.4", "G": "03.12.04", "H": "Withdrawn", "I": "Incorporated into 03.15.02.", "O": "X"},
            {"C": "", "A": "", "G": "03.15.01\t", "H": "Policy and Procedures", "I": "a.\tDevelop policies.\n\n",
             "N": "X"}]
    cat, xw = convert(rows)
    assert cat == [{"id": "03.15.01", "family": "Planning", "family_code": "PL", "title": "Policy and Procedures",
                    "requirement": "a. Develop policies."}]
    assert xw == [{"rev2_id": "3.2.3", "rev3_ids": "03.02.01", "change": "withdrawn",
                   "note": "Incorporated into 03.02.01."}]


def test_load_refuses_an_unpinned_file(tmp_path):
    p = tmp_path / "x.xlsx"
    p.write_bytes(b"not the NIST file")
    with pytest.raises(SystemExit, match="refusing"):
        load(str(p))
