# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""import_catalog_r2.py SOURCE: build rev2/catalog.csv from NIST's SP 800-171 Rev 2 requirements CSV.

SOURCE is the NIST URL or a local copy. The file's sha256 must match the pinned value; publication order is kept."""
import csv
import hashlib
import io
import sys
import urllib.request
from pathlib import Path

URL = "https://csrc.nist.gov/files/pubs/sp/800/171/r2/upd1/final/docs/sp800-171r2-security-reqs.csv"
SHA256 = "0f4d59413bbcc9998da80495ce46ebfe0475e392803c4d2ed38d9941d83f138d"
CODES = {"Access Control": "AC", "Awareness and Training": "AT", "Audit and Accountability": "AU",
         "Configuration Management": "CM", "Identification and Authentication": "IA", "Incident Response": "IR",
         "Maintenance": "MA", "Media Protection": "MP", "Personnel Security": "PS", "Physical Protection": "PE",
         "Risk Assessment": "RA", "Security Assessment": "CA", "System and Communications Protection": "SC",
         "System and Information Integrity": "SI"}
CANON = {k.lower(): k for k in CODES}
OUT = Path(__file__).resolve().parents[1] / "rev2" / "catalog.csv"


def load(source):
    if source.startswith("https://"):
        with urllib.request.urlopen(source, timeout=60) as r:
            data = r.read()
    else:
        data = Path(source).read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != SHA256:
        sys.exit(f"refusing: sha256 {got} is not the pinned NIST file {SHA256}")
    return data.decode("utf-8-sig")


def convert(text):
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        fam = CANON[r["Family"].lower()]      # NIST's CSV is inconsistent in case (e.g. "Incident response")
        out.append({"id": r["Identifier"], "family": fam, "family_code": CODES[fam],
                    "basic_derived": r["Basic/Derived Security Requirement"], "requirement": r["Security Requirement"]})
    return out


def main(argv):
    rows = convert(load(argv[1] if len(argv) > 1 else URL))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "family", "family_code", "basic_derived", "requirement"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {OUT}: {len(rows)} requirements")


if __name__ == "__main__":
    main(sys.argv)
