import ast
import os
from pathlib import Path

import pytest
from render.chpfill import load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]


def test_code_parses_as_python_3_9():
    for p in list((TOP / "render").glob("*.py")) + list((TOP / "tools").glob("*.py")):
        ast.parse(p.read_text(), filename=str(p), feature_version=(3, 9))


@pytest.mark.skipif(not os.environ.get("CHP_AC_KEYS"), reason="set CHP_AC_KEYS to the owner's private AC key list")
def test_automated_compliance_contract():
    """Every Automated_Compliance in-use key that our vocabulary also defines keeps the SAME name (no near-duplicates)."""
    ac = [k.strip() for k in Path(os.environ["CHP_AC_KEYS"]).read_text().splitlines() if k.strip()]
    vocab = load_vocabulary(TOP / "vocabulary.md")
    for k in ac:
        concrete = k.replace("<n>", "1").replace("<name>", "example")
        if vocab_entry(concrete, vocab) is None:
            continue
        assert k in vocab, f"{k}: matched by a different vocabulary name"
