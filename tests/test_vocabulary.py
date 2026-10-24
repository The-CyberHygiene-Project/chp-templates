import re
from pathlib import Path

import pytest
from render.chpfill import FillError, check_values, load_vocabulary

VOC = Path(__file__).resolve().parents[1] / "vocabulary.md"


def test_rows_well_formed_and_unique():
    v = load_vocabulary(VOC)
    assert v and len(v) == len(set(v))
    for name, row in v.items():
        assert re.fullmatch(r"[a-z][a-z0-9_]*(\.([a-z0-9_]+|<n>|<name>))+", name), name
        assert row["kind"] in {"value", "list", "fact"} and row["visibility"] in {"public", "private", "never-to-ai"}
        assert row["meaning"]


def test_public_mode_refuses_private_values():
    v = load_vocabulary(VOC)
    with pytest.raises(FillError, match="roles.security_officer is private: not placed in a public copy"):
        check_values({"roles.security_officer": "A. Person"}, {}, v, public=True)
    check_values({"organization.name": "Example Manufacturing LLC"}, {}, v, public=True)


def test_unknown_profile_key_refused_and_patterns_match():
    v = load_vocabulary(VOC)
    with pytest.raises(FillError, match="organisation.name is not in vocabulary.md"):
        check_values({"organisation.name": "x"}, {}, v, public=False)
    check_values({"contract.12.label": "x"}, {}, v, public=False)
    with pytest.raises(FillError, match="contract.x.label"):
        check_values({"contract.x.label": "x"}, {}, v, public=False)
