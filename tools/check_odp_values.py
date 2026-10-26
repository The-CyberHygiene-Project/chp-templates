# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""check_odp_values.py MEMO.pdf [--show]: check rev3/odp-values.csv against the DoD ODP memo (developer tool; needs
pdftotext). The memo's sha256 must match the pinned copy. Every memo ODP ID must be in the CSV exactly once; each row's
assignment and value words must appear, in order, in that ID's table row; the guidance count must match the memo."""
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

SHA256 = "fd83ecf4e0998f0b29d5e6f222e7364ce67eb6fdedb5ac4f34ec4310ba495916"
TOP = Path(__file__).resolve().parents[1]
ROW_ID = re.compile(r"^\s*(03\.\d\d\.\d\d(?:\.[a-z0-9]+)*)(?=\s|$)")


def words(text):
    # split at hyphens on both sides, so "organization-defined" matches a cell wrapped as "organization-" / "defined"
    text = re.sub(r"significant1|providers2", lambda m: m.group(0)[:-1], text).replace("-", "- ")
    return text.replace("[", " [ ").replace("]", " ] ").split()


def in_order(needle, hay):
    it = iter(hay)
    return all(w in it for w in needle)


def windows(lines):
    """{odp_id: the table lines from just after the previous row to just before the next one}."""
    marks = [(i, m.group(1)) for i, ln in enumerate(lines) if (m := ROW_ID.match(ln)) and "(" not in ln[:20]]
    out = {}
    for n, (i, oid) in enumerate(marks):
        start = marks[n - 1][0] + 1 if n else max(0, i - 15)
        end = marks[n + 1][0] if n + 1 < len(marks) else i + 15
        out[oid] = lines[start:end]
    return out


def check(pdf, show=False):
    data = Path(pdf).read_bytes()
    if hashlib.sha256(data).hexdigest() != SHA256:
        return ["memo: sha256 is not the pinned copy"]
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    lines = text.split("\n")
    memo_ids = set(re.findall(r"\((03\.\d\d\.\d\d[^)\s]*)\)", text))
    rows = list(csv.DictReader(open(TOP / "rev3/odp-values.csv", encoding="utf-8")))
    ids = [r["odp_id"] for r in rows]
    bad = [f"duplicate {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    bad += [f"missing from CSV: {i}" for i in sorted(memo_ids - set(ids))]
    bad += [f"not in memo: {i}" for i in sorted(set(ids) - memo_ids)]
    if sum(r["kind"] == "guidance" for r in rows) != text.count("Guidance:"):
        bad.append("guidance count differs from the memo")
    win = windows(lines)
    for r in rows:
        w = win.get(r["odp_id"])
        if w is None:
            bad.append(f"{r['odp_id']}: no table row found")
            continue
        hay = words(" ".join(w))
        for field in ("assignment", "value"):
            if not in_order(words(r[field]), hay):
                bad.append(f"{r['odp_id']}: {field} words not found in order in its table row")
        if show:
            print(f"== {r['odp_id']} [{r['kind']}]\n  CSV:  {r['value']}\n  MEMO: {' '.join(' '.join(w).split())}")
    return bad


if __name__ == "__main__":
    problems = check(sys.argv[1], "--show" in sys.argv)
    print("\n".join(problems) if problems else f"ODP OK: rev3/odp-values.csv matches the DoD memo")
    sys.exit(1 if problems else 0)
