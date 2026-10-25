"""Owner 2026-10-25: contracts follow Automated_Compliance's committed contract.<n>.* form (list derived); the AC draft's
extra names are reserved in vocabulary.md under the same names."""
from pathlib import Path

from render.chpfill import check_values, load_values, load_vocabulary

TOP = Path(__file__).resolve().parents[1]
MAP = TOP / "site-conf-mapping.csv"
VOC = load_vocabulary(TOP / "vocabulary.md")
AC_CONTRACT = ("label", "agency_group", "vehicle", "information", "clauses", "required_revision", "revision_basis",
               "last_verified")


def load(tmp_path, text):
    p = tmp_path / "p.ini"
    p.write_text(text)
    return load_values(p, None, None, MAP)


def test_contract_list_is_derived_in_number_order(tmp_path):
    v, _, prov = load(tmp_path, "[contract.2]\nlabel = Second PO\n\n[contract.1]\nlabel = First PO\n"
                                "clauses = DFARS 252.204-7012\n\n[contract.3]\nvehicle = no label here\n")
    assert v["contract.list"] == ["First PO (DFARS 252.204-7012)", "Second PO", "contract 3"]
    assert prov["contract.list"] == "derived from contract.<n> entries"


def test_deprecated_contract_list_still_works_alone(tmp_path):
    v, _, prov = load(tmp_path, "[contract]\nlist =\n    Old PO\n")
    assert v["contract.list"] == ["Old PO"] and prov["contract.list"] == "profile"


def test_ac_contract_names_are_in_the_vocabulary(tmp_path):
    for f in AC_CONTRACT:
        assert f"contract.<n>.{f}" in VOC and VOC[f"contract.<n>.{f}"]["visibility"] == "private", f


def test_reserved_draft_names_are_present_and_marked():
    reserved = [k for k, r in VOC.items() if r["meaning"].startswith("RESERVED")]
    for k in ("decision.log_review_frequency", "decision.visitor_log_required", "facts.has_mail_service",
              "facts.uses_external_ai", "site.directory_base", "site.host.<name>.address", "organization.owner_name"):
        assert k in reserved, k


def test_reserved_names_are_accepted_in_a_profile(tmp_path):
    v, f, _ = load(tmp_path, "[decision]\nvisitor_log_required = yes\n\n[facts]\nhas_mail_service = no\n")
    check_values(v, f, VOC, public=False)
