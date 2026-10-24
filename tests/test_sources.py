from pathlib import Path

import pytest
from render.chpfill import FillError, load_values

TOP = Path(__file__).resolve().parents[1]
MAP = TOP / "site-conf-mapping.csv"
PROFILE = """[organization]
name = Example Manufacturing LLC
reviewers =
    Smith, J.
    Lee, K.

[facts]
has_wireless = no
has_nas = Yes

[contract.1]
label = Example contract
"""


def write(tmp_path, name, text, raw=False):
    p = tmp_path / name
    (p.write_bytes(text) if raw else p.write_text(text))
    return p


def test_profile_values_lists_facts_and_dotted_sections(tmp_path):
    v, f, prov = load_values(write(tmp_path, "p.ini", PROFILE), None, None, MAP)
    assert v["organization.name"] == "Example Manufacturing LLC"
    assert v["organization.reviewers"] == ["Smith, J.", "Lee, K."]
    assert f == {"facts.has_wireless": False, "facts.has_nas": True}
    assert v["contract.1.label"] == "Example contract" and prov["organization.name"] == "profile"


def test_bad_fact_value_is_an_error(tmp_path):
    with pytest.raises(FillError, match="facts.has_nas"):
        load_values(write(tmp_path, "p.ini", "[facts]\nhas_nas = maybe\n"), None, None, MAP)


def test_site_conf_fills_only_what_the_profile_lacks(tmp_path):
    p = write(tmp_path, "p.ini", "[site]\ntimezone = UTC\n")
    s = write(tmp_path, "site.conf", "# comment\nDOMAIN=example.test\nTIMEZONE=America/Denver\nSUBNET=192.0.2.0/24\n")
    v, _, prov = load_values(p, s, None, MAP)
    assert v["site.domain"] == "example.test" and prov["site.domain"] == "site.conf"
    assert v["site.timezone"] == "UTC" and prov["site.timezone"] == "profile"
    assert v["site.lan_subnet"] == "192.0.2.0/24"


def test_defaults_are_marked_unconfirmed(tmp_path):
    d = write(tmp_path, "defaults.ini", "[decision]\nlockout_threshold = 5\n")
    p = write(tmp_path, "p.ini", "[decision]\npatch_cadence = monthly\n")
    v, _, prov = load_values(p, None, d, MAP)
    assert v["decision.lockout_threshold"] == "5" and prov["decision.lockout_threshold"] == "default (not yet confirmed)"
    assert prov["decision.patch_cadence"] == "profile"


def test_profile_with_bom_crlf_and_trailing_space(tmp_path):
    clean = load_values(write(tmp_path, "a.ini", PROFILE), None, None, MAP)
    messy = PROFILE.replace("\n", "  \r\n").encode("utf-8")
    other = load_values(write(tmp_path, "b.ini", b"\xef\xbb\xbf" + messy, raw=True), None, None, MAP)
    assert clean == other


@pytest.mark.parametrize("val", ["password: hunter2", "token=abc123def", "Secret = s3cr3t", "BEGIN OPENSSH PRIVATE KEY", "A" * 40])
def test_secrets_refused(tmp_path, val):
    with pytest.raises(FillError) as e:
        load_values(write(tmp_path, "p.ini", f"[organization]\nnote = {val}\n"), None, None, MAP)
    assert "organization.note" in str(e.value) and val not in str(e.value)


def test_ordinary_text_mentioning_password_is_accepted(tmp_path):
    v, _, _ = load_values(write(tmp_path, "p.ini", "[policies]\nlist =\n    Identification and Authentication (Password) Policy v1.0\n    Access Token Handling Procedure\n"), None, None, MAP)
    assert v["policies.list"][0].startswith("Identification")


def test_a_key_named_like_a_secret_is_refused(tmp_path):
    with pytest.raises(FillError, match="organization.admin_password"):
        load_values(write(tmp_path, "p.ini", "[organization]\nadmin_password = x\n"), None, None, MAP)
