"""Owner ruling 2026-10-25: systems follow Automated_Compliance's committed one-entry-per-system form
(system.<name>.kind|in_boundary|operating_system|administered_by|provider). The renderer derives the boundary list."""
from pathlib import Path

import pytest
from render.chpfill import FillError, check_values, load_values, load_vocabulary

TOP = Path(__file__).resolve().parents[1]
MAP = TOP / "site-conf-mapping.csv"
PROFILE = """[system.srv1]
kind = identity server
in_boundary = yes
operating_system = Rocky Linux 9
administered_by = Sam Sample

[system.printer]
kind = network printer
in_boundary = no

[system.ws1]
in_boundary = Yes
operating_system = Rocky Linux 9

[system.ws2]
in_boundary = yes
"""


def load(tmp_path, text):
    p = tmp_path / "p.ini"
    p.write_text(text)
    return load_values(p, None, None, MAP)


def test_boundary_list_is_derived_in_profile_order(tmp_path):
    v, _, prov = load(tmp_path, PROFILE)
    assert v["systems.in_boundary"] == ["srv1 (identity server, Rocky Linux 9)", "ws1 (Rocky Linux 9)", "ws2"]
    assert prov["systems.in_boundary"] == "derived from system.<name> entries"
    assert v["system.srv1.administered_by"] == "Sam Sample"


def test_per_system_entries_win_over_the_deprecated_list(tmp_path):
    v, _, _ = load(tmp_path, PROFILE + "\n[systems]\nin_boundary =\n    old one\n")
    assert v["systems.in_boundary"][0].startswith("srv1")


def test_the_deprecated_list_still_works_alone(tmp_path):
    v, _, prov = load(tmp_path, "[systems]\nin_boundary =\n    a\n    b\n")
    assert v["systems.in_boundary"] == ["a", "b"] and prov["systems.in_boundary"] == "profile"


def test_in_boundary_must_be_yes_or_no(tmp_path):
    with pytest.raises(FillError, match="system.srv1.in_boundary"):
        load(tmp_path, "[system.srv1]\nin_boundary = maybe\n")


def test_ac_names_are_in_the_vocabulary(tmp_path):
    v, f, _ = load(tmp_path, PROFILE)
    check_values(v, f, load_vocabulary(TOP / "vocabulary.md"), public=False)
    vocab = load_vocabulary(TOP / "vocabulary.md")
    for field in ("kind", "in_boundary", "operating_system", "administered_by", "provider"):
        assert f"system.<name>.{field}" in vocab and vocab[f"system.<name>.{field}"]["visibility"] == "private"
