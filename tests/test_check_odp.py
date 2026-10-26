import csv
import os
import shutil
from pathlib import Path

import pytest

import tools.check_odp_values as chk

MEMO = Path(os.environ.get("DOD_ODP_MEMO", str(Path.home() / "rag-library/documents-sysadmin/2026-10/DOD 800-171 ODP guidance.pdf")))
need = pytest.mark.skipif(not (MEMO.exists() and shutil.which("pdftotext")), reason="needs the DoD memo and pdftotext")


@need
def test_committed_values_pass():
    assert chk.check(str(MEMO)) == []


@need
def test_a_dropped_clause_is_reported(tmp_path, monkeypatch):
    # final review I3: an in-order check alone passed a shortened value
    rows = list(csv.DictReader(open(chk.TOP / "rev3/odp-values.csv", encoding="utf-8")))
    for r in rows:
        if r["odp_id"] == "03.05.07.f":
            r["value"] = "1) Must have a minimum length of 16 characters."
    (tmp_path / "rev3").mkdir()
    with open(tmp_path / "rev3/odp-values.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    monkeypatch.setattr(chk, "TOP", tmp_path)
    assert any(p.startswith("03.05.07.f:") for p in chk.check(str(MEMO)))
