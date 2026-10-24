# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""evidence_index.py --scan X.xml [...] --catalog rev2/catalog.csv [--out out/evidence-r2.md]

An authoring aid, not shipped content: for each SP 800-171 requirement, the OpenSCAP rules from the appliance's scan
results that cite it, split into pass and fail. A rule cites a requirement through an XCCDF <reference> whose href
names SP 800-171."""
import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://checklists.nist.gov/xccdf/1.2}"


def index(paths):
    """{requirement id: {"pass": [(rule id, title)], "fail": [...]}} across all scan results."""
    out = {}
    for path in paths:
        root = ET.parse(path).getroot()
        rules = {}
        for rule in root.iter(NS + "Rule"):
            ids = []
            for ref in rule.findall(NS + "reference"):
                if "800-171" in (ref.get("href") or "") and ref.text:
                    ids += [x.strip() for x in ref.text.split(",") if x.strip()]
            if ids:
                rules[rule.get("id")] = (rule.findtext(NS + "title", default="").strip(), ids)
        for tr in root.iter(NS + "TestResult"):
            for rr in tr.findall(NS + "rule-result"):
                rid, res = rr.get("idref"), rr.findtext(NS + "result")
                if rid in rules and res in ("pass", "fail"):
                    title, ids = rules[rid]
                    for i in ids:
                        bucket = out.setdefault(i, {"pass": [], "fail": []})[res]
                        if (rid, title) not in bucket:
                            bucket.append((rid, title))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", nargs="+", required=True)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--out", default="out/evidence-r2.md")
    a = ap.parse_args(argv)
    idx = index(a.scan)
    lines = ["# Scan evidence per requirement (authoring aid; not shipped)", ""]
    with open(a.catalog, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            e = idx.get(r["id"])
            if not e:
                continue
            lines.append(f"## {r['id']} {r['requirement'][:80]}")
            lines += [f"- pass: `{rid}` {t}" for rid, t in e["pass"]]
            lines += [f"- **FAIL**: `{rid}` {t}" for rid, t in e["fail"]]
            lines.append("")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {a.out}: {sum(1 for _ in idx)} requirements with scan evidence")


if __name__ == "__main__":
    main()
