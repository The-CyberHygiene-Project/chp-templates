import csv
import os
import re
from pathlib import Path

import pytest
from render.chpfill import TOKEN, load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]
CTRL = TOP / "rev2/templates/ssp/controls"
HEAD = re.compile(r"^<!-- chp:control id=(\S+) status=(appliance|site|partial) evidence=(\S*) -->\n")
IDS = [r["id"] for r in csv.DictReader(open(TOP / "rev2/catalog.csv", encoding="utf-8"))]


def blocks():
    return {p.stem: p.read_text() for p in CTRL.glob("*.md")}


def test_one_block_per_catalog_requirement():
    assert sorted(blocks()) == sorted(IDS)


@pytest.mark.parametrize("cid", IDS)
def test_block_header_status_and_sections(cid):
    text = (CTRL / f"{cid}.md").read_text()
    m = HEAD.match(text)
    assert m and m.group(1) == cid, "bad header"
    status, evidence = m.group(2), m.group(3)
    if status in ("appliance", "partial"):
        assert evidence, "appliance/partial must cite evidence"
    assert "\n**Implementation:** " in text and "\n**Site responsibility:** " in text
    site = text.split("**Site responsibility:** ", 1)[1].strip()
    assert site, "empty site responsibility"
    if status == "site":
        assert site != "None beyond operating the appliance as documented."
    assert not re.search(r"\*\*\d+/110\*\*", text)
    v = load_vocabulary(TOP / "vocabulary.md")
    assert all(vocab_entry(t.group(1), v) for t in TOKEN.finditer(text))


@pytest.mark.skipif(not os.environ.get("IDM_ASSISTANT"), reason="set IDM_ASSISTANT to the idm-assistant checkout")
def test_evidence_paths_exist():
    root = Path(os.environ["IDM_ASSISTANT"])
    for cid, text in blocks().items():
        for item in HEAD.match(text).group(3).split(";"):
            if item and not item.startswith("scan:"):
                assert (root / item.split("#")[0]).exists(), f"{cid}: {item}"
