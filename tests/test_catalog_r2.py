import csv
from pathlib import Path

CAT = Path(__file__).resolve().parents[1] / "rev2" / "catalog.csv"
CODES = {"Access Control": "AC", "Awareness and Training": "AT", "Audit and Accountability": "AU",
         "Configuration Management": "CM", "Identification and Authentication": "IA", "Incident Response": "IR",
         "Maintenance": "MA", "Media Protection": "MP", "Personnel Security": "PS", "Physical Protection": "PE",
         "Risk Assessment": "RA", "Security Assessment": "CA", "System and Communications Protection": "SC",
         "System and Information Integrity": "SI"}


def rows():
    return list(csv.DictReader(open(CAT, encoding="utf-8")))


def test_110_requirements_14_families_in_publication_order():
    r = rows()
    assert len(r) == 110 and len({x["family_code"] for x in r}) == 14
    assert r[0]["id"] == "3.1.1" and r[-1]["id"] == "3.14.7"
    assert all(CODES[x["family"]] == x["family_code"] for x in r)


def test_ids_unique_and_text_clean():
    r = rows()
    assert len({x["id"] for x in r}) == 110
    assert all(x["requirement"] == x["requirement"].strip() and x["requirement"] for x in r)
