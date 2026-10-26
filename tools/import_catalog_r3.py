# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""import_catalog_r3.py SOURCE: build rev3/catalog.csv and rev3/crosswalk.csv from NIST's SP 800-171 Rev 2 to Rev 3
change analysis workbook (one pinned file gives both). SOURCE is the NIST URL or a local copy; its sha256 must match."""
import csv
import hashlib
import io
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

URL = "https://csrc.nist.gov/files/pubs/sp/800/171/r3/final/docs/sp800-171r2-to-r3-analysis.xlsx"
SHA256 = "ad0908f52945e316dec05a4032cbcaa75958eab2534d2627b3a89f696fb30b84"
SHEET = "xl/worksheets/sheet2.xml"          # "Change Analysis 800-171 R2-R3" (pinned file, so the position is fixed)
FAMILIES = {"01": ("Access Control", "AC"), "02": ("Awareness and Training", "AT"),
            "03": ("Audit and Accountability", "AU"), "04": ("Configuration Management", "CM"),
            "05": ("Identification and Authentication", "IA"), "06": ("Incident Response", "IR"),
            "07": ("Maintenance", "MA"), "08": ("Media Protection", "MP"), "09": ("Personnel Security", "PS"),
            "10": ("Physical Protection", "PE"), "11": ("Risk Assessment", "RA"),
            "12": ("Security Assessment and Monitoring", "CA"), "13": ("System and Communications Protection", "SC"),
            "14": ("System and Information Integrity", "SI"), "15": ("Planning", "PL"),
            "16": ("System and Services Acquisition", "SA"), "17": ("Supply Chain Risk Management", "SR")}
# NIST erratum: the withdrawn 03.12.04 row is labelled with Rev 2 ID 3.11.4, which does not exist in Rev 2.
# Rev 2 3.12.4 has its own row (mapped to 03.15.02), so this row is skipped.
ERRATA = {("3.11.4", "03.12.04")}
R3ID = re.compile(r"03\.(\d\d)[ .](\d\d)")
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
TOP = Path(__file__).resolve().parents[1]


def load(source):
    if source.startswith("https://"):
        with urllib.request.urlopen(source, timeout=60) as r:
            data = r.read()
    else:
        data = Path(source).read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != SHA256:
        sys.exit(f"refusing: sha256 {got} is not the pinned NIST file {SHA256}")
    return data


def read_rows(data):
    """Every sheet row as {column letter: text}."""
    z = zipfile.ZipFile(io.BytesIO(data))
    shared = ["".join(t.text or "" for t in si.iter(M + "t"))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si")]
    rows = []
    for r in ET.fromstring(z.read(SHEET)).iter(M + "row"):
        d = {}
        for c in r.findall(M + "c"):
            v = c.find(M + "v")
            col = re.sub(r"\d", "", c.get("r"))
            d[col] = "" if v is None else (shared[int(v.text)] if c.get("t") == "s" else v.text)
        rows.append(d)
    return rows


def _lines(text):
    return "\n".join(ln.replace("\t", " ").strip() for ln in text.replace("\r", "").split("\n") if ln.strip())


def _change(r):
    if r.get("O", "").strip() == "X":
        return "withdrawn"
    for col, name in (("J", "no significant change"), ("K", "significant change"), ("L", "minor change")):
        if r.get(col, "").strip() == "X":
            return name
    raise ValueError(f"row for {r.get('C')} / {r.get('G')} has no change type")


def _key(rev2_id):
    return tuple(int(p) for p in rev2_id.split("."))


def convert(rows):
    catalog, crosswalk = [], []
    for r in rows[1:]:
        r2, r3 = r.get("C", "").strip(), r.get("G", "").strip()
        if (r2, r3) in ERRATA:
            continue
        withdrawn = r.get("O", "").strip() == "X"
        if not withdrawn and r3:
            fam, code = FAMILIES[r3[3:5]]
            catalog.append({"id": r3, "family": fam, "family_code": code, "title": r.get("H", "").strip(),
                            "requirement": _lines(r.get("I", ""))})
        if r2:
            if withdrawn:
                note = re.sub(r"^Withdrawn\s+", "", " ".join(_lines(r.get("I", "")).split("\n")))
                note = R3ID.sub(lambda m: f"03.{m.group(1)}.{m.group(2)}", note)
                targets = sorted(set(re.findall(r"03\.\d\d\.\d\d", note)))
            else:
                note, targets = " ".join(_lines(r.get("P", "")).split("\n")), [r3]   # one line per note
            crosswalk.append({"rev2_id": r2, "rev3_ids": " ".join(targets), "change": _change(r), "note": note})
    catalog.sort(key=lambda x: x["id"])
    crosswalk.sort(key=lambda x: _key(x["rev2_id"]))
    return catalog, crosswalk


def write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    cat, xw = convert(read_rows(load(sys.argv[1] if len(sys.argv) > 1 else URL)))
    (TOP / "rev3").mkdir(exist_ok=True)
    write(TOP / "rev3/catalog.csv", ["id", "family", "family_code", "title", "requirement"], cat)
    write(TOP / "rev3/crosswalk.csv", ["rev2_id", "rev3_ids", "change", "note"], xw)
    print(f"wrote rev3/catalog.csv ({len(cat)} requirements) and rev3/crosswalk.csv ({len(xw)} Rev 2 IDs)")
