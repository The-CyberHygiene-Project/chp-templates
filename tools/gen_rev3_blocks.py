# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""gen_rev3_blocks.py: write a 'pending' Rev 3 control block for every catalog requirement that has none. Existing
blocks are never touched: later batches edit them by hand as the Rev 3 reference implementation proves each control."""
import csv
from pathlib import Path

from tools.odp_tables import key

TOP = Path(__file__).resolve().parents[1]
CTRL = TOP / "rev3/templates/ssp/controls"


def _csv(name):
    return list(csv.DictReader(open(TOP / "rev3" / name, encoding="utf-8")))


def rev2_basis(crosswalk):
    out = {}
    for r in crosswalk:
        for t in r["rev3_ids"].split():
            prim, also = out.setdefault(t, ([], []))
            (also if r["change"] == "withdrawn" else prim).append(r["rev2_id"])
    return out


def _basis_line(primary, also):
    if not primary and not also:
        return "**Rev 2 basis:** none; this requirement is new in Rev 3."
    if len(primary) == 1 and not also:
        return (f"**Rev 2 basis:** {primary[0]}. For the appliance's implementation today, see the Rev 2 plan's "
                f"narrative for {primary[0]}.")
    head = ", ".join(primary) if primary else "none directly"
    tail = f"; it also covers withdrawn {', '.join(also)}" if also else ""
    return (f"**Rev 2 basis:** {head}{tail}. For the appliance's implementation today, see the Rev 2 plan's narratives "
            "for those requirements.")


def block_text(cid, basis, odps):
    parts = [f"<!-- chp:control id={cid} status=pending evidence= -->\n"
             "**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, "
             "so this library does not yet describe the appliance's implementation.",
             _basis_line(*basis)]
    if odps:
        lines = ["**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):", ""]
        for r in odps:
            ln = f"- `{r['odp_id']}` {r['assignment']}: {{{{{key(r['odp_id'])}}}}}"
            if r["kind"] == "guidance":
                ln += f" *DoD gives guidance, not a value: {r['value'].replace('Guidance:', '', 1).strip()}*"
            lines.append(ln)
        parts.append("\n".join(lines))
    parts.append("**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 "
                 "text is written.")
    return "\n\n".join(parts) + "\n"


def main(force=False):
    CTRL.mkdir(parents=True, exist_ok=True)
    basis, odps, wrote = rev2_basis(_csv("crosswalk.csv")), _csv("odp-values.csv"), 0
    for r in _csv("catalog.csv"):
        p = CTRL / f"{r['id']}.md"
        if p.exists() and not force:
            continue
        p.write_text(block_text(r["id"], basis.get(r["id"], ([], [])),
                                [o for o in odps if o["requirement_id"] == r["id"]]), encoding="utf-8")
        wrote += 1
    return wrote


if __name__ == "__main__":
    print(f"wrote {main()} pending Rev 3 control blocks")
