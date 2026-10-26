# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""check_odp_values.py MEMO.pdf [--show]: check rev3/odp-values.csv against the DoD ODP memo (developer tool; needs
pdftotext). The memo's sha256 must match the pinned copy. Every memo ODP ID must be in the CSV exactly once; each row's
assignment and value words must appear, in order, in that ID's table row; the guidance count must match the memo."""
import csv
import hashlib
import io
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


def _cells(pdf):
    """{odp_id: the ODP Value cell's text}, read by word position (pdftotext -tsv), footnote superscripts dropped.
    A table continued on a new page gives the lines above its first row to the previous page's last row."""
    tsv = subprocess.run(["pdftotext", "-tsv", pdf, "-"], capture_output=True, text=True, check=True).stdout
    words = [r for r in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE)
             if r["level"] == "5" and float(r["height"]) >= 8]
    for w in words:
        for k in ("left", "top", "height"):
            w[k] = float(w[k])
    pages = {}
    for w in words:
        pages.setdefault(int(w["page_num"]), []).append(w)
    out, last = {}, None
    for _, ws in sorted(pages.items()):
        prev_top = -1.0
        for ih in sorted((w for w in ws if w["text"] == "Identifier"), key=lambda w: w["top"]):
            hdr = [w for w in ws if abs(w["top"] - ih["top"]) < 25]
            val = [w for w in hdr if w["text"] == "Value"]
            if not val:
                continue
            vx = max([w["left"] for w in hdr if w["text"] == "ODP" and abs(w["top"] - val[0]["top"]) < 3
                      and w["left"] < val[0]["left"]] or [val[0]["left"]])
            idl = min(w["left"] for w in hdr if w["text"] in ("ODP", "Identifier") and w["left"] <= ih["left"] + 1
                      and abs(w["top"] - ih["top"]) < 16)
            hb = max(w["top"] + w["height"] for w in hdr if w["text"] in ("Identifier", "Value", "Assignment", "Text", "ODP"))
            body = sorted((w for w in ws if w["top"] > hb + 1), key=lambda w: (w["top"], w["left"]))
            end = next((w["top"] for w in body if w["left"] < idl - 8 or w["text"] == "Identifier"), None)
            body = [w for w in body if (end is None or w["top"] < end - 0.5)
                    and not (w["text"].isdigit() and w["top"] > 700)]
            ids = [w for w in body if re.fullmatch(r"03\.\d\d\.\d\d(?:\.[a-z0-9]+)*", w["text"]) and w["left"] < vx - 40]
            cont = not any(w["text"] == "Values" and prev_top < w["top"] < ih["top"] for w in ws)
            prev_top = ih["top"]
            vals = [w for w in body if w["left"] >= vx - 2]
            lines = sorted({round(w["top"], 1) for w in vals})
            def gap_split(lo, hi):
                c = [ln for ln in lines if lo < ln < hi]
                g = [(c[k + 1] - c[k], (c[k + 1] + c[k]) / 2) for k in range(len(c) - 1)]
                return max(g)[1] if g else (lo + hi) / 2
            bounds = [gap_split(a["top"] - 40, b["top"] + 40) for a, b in zip(ids, ids[1:])]
            bounds = [b if ids[k]["top"] - 1 <= b <= ids[k + 1]["top"] + 1 else (ids[k]["top"] + ids[k + 1]["top"]) / 2
                      for k, b in enumerate(bounds)]
            lo = [-1.0] + bounds
            if cont and ids and last:              # continuation: text above the first row's own cell
                split = gap_split(hb, ids[0]["top"] + 1)
                out[last] += " " + _join([w for w in vals if w["top"] < split])
                lo[0] = split
            hi = bounds + [1e9]
            for n, i in enumerate(ids):
                out[i["text"]] = _join([w for w in vals if lo[n] < w["top"] < hi[n]])
            if ids:
                last = ids[-1]["text"]
    return out


def _join(ws):
    lines = []
    for w in sorted(ws, key=lambda w: w["top"]):
        if lines and abs(w["top"] - lines[-1][0]) < 4:
            lines[-1][1].append(w)
        else:
            lines.append([w["top"], [w]])
    return " ".join(x["text"] for _, ln in lines for x in sorted(ln, key=lambda w: w["left"]))


def norm(text):
    """Compare form: whitespace collapsed, line-wrap hyphens joined, no space before punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(\w)- (\w)", r"\1-\2", text)
    return re.sub(r" ([),.;:])", r"\1", text)


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
    win, cells = windows(lines), _cells(pdf)
    for r in rows:
        w = win.get(r["odp_id"])
        if w is None:
            bad.append(f"{r['odp_id']}: no table row found")
            continue
        hay = words(" ".join(w))
        for field in ("assignment", "value"):
            if not in_order(words(r[field]), hay):
                bad.append(f"{r['odp_id']}: {field} words not found in order in its table row")
        if norm(r["value"]) != norm(cells.get(r["odp_id"], "")):
            bad.append(f"{r['odp_id']}: value differs from its ODP Value cell (a word dropped, added or changed)")
        if show:
            print(f"== {r['odp_id']} [{r['kind']}]\n  CSV:  {r['value']}\n  MEMO: {' '.join(' '.join(w).split())}")
    return bad


if __name__ == "__main__":
    problems = check(sys.argv[1], "--show" in sys.argv)
    print("\n".join(problems) if problems else f"ODP OK: rev3/odp-values.csv matches the DoD memo")
    sys.exit(1 if problems else 0)
