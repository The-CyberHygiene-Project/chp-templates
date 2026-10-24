import re
from pathlib import Path

from render.chpfill import TOKEN, load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]
FRAME = (TOP / "rev2/templates/ssp/frame.md").read_text()
ORDER = ["## DOCUMENT CONTROL", "## EXECUTIVE SUMMARY", "## 2. SYSTEM IDENTIFICATION", "## 3. SYSTEM DESCRIPTION",
         "## 4. SECURITY CONTROL IMPLEMENTATION", "## 5. CONTINGENCY PLANNING (CP)", "## 6. SECURITY POLICIES AND PROCEDURES",
         "## 10. PLAN OF ACTION AND MILESTONES (POA&M)", "## 11. IMPLEMENTATION METRICS", "## 12. CONCLUSION",
         "## AUTHORIZATION", "## APPENDICES"]


def test_sections_in_order_and_7_to_9_absent():
    pos = [FRAME.index(h + "\n") for h in ORDER]
    assert pos == sorted(pos)
    assert not re.search(r"^## [789]\.", FRAME, re.M)


def test_revision_history_layout_is_exact():
    assert "| Version | Date | Author | Description |\n|:---|:---|:---|:---|\n" in FRAME


def test_two_separate_score_cards_without_scores():
    assert "{{assessment.sprs_score}}" in FRAME and "{{assessment.sprs_basis}}" in FRAME
    assert "| **Strict 800-171A objectives met** |" in FRAME and "{{assessment.objectives_met}}" in FRAME
    assert not re.search(r"\*\*\d+/110\*\*", FRAME)


def test_each_include_once_and_open_appendices():
    for inc in ("{{> arch}}", "{{> controls}}", "{{> family_status}}"):
        assert FRAME.count(inc) == 1, inc
    assert FRAME.rstrip().endswith("*Add further lettered appendices below; nothing reads their order.*")


def test_every_placeholder_is_in_the_vocabulary():
    v = load_vocabulary(TOP / "vocabulary.md")
    missing = sorted({m.group(1) for m in TOKEN.finditer(FRAME)} - {k for k in {m.group(1) for m in TOKEN.finditer(FRAME)}
                                                                    if vocab_entry(k, v)})
    facts = sorted(set(re.findall(r"\{\{#if (facts\.[a-z0-9_]+)\}\}", FRAME)))
    missing += [f for f in facts if not vocab_entry(f, v)]
    assert missing == []
