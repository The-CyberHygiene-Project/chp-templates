from pathlib import Path

from render.chpfill import DEFAULT, _status_line, assemble, load_values

TOP = Path(__file__).resolve().parents[1]
MAP = TOP / "site-conf-mapping.csv"


def lib(tmp_path, catalog, block):
    t = tmp_path / "lib" / "templates"
    (t / "ssp" / "controls").mkdir(parents=True)
    (t / "ssp" / "arch").mkdir()
    (t / "poam").mkdir()
    (t / "ssp" / "frame.md").write_text("{{> controls}}\n")
    (t / "ssp" / "arch" / "chp-appliance.md").write_text("arch\n")
    (t / "poam" / "frame.md").write_text("poam\n")
    (tmp_path / "lib" / "catalog.csv").write_text(catalog)
    for cid, text in block.items():
        (t / "ssp" / "controls" / f"{cid}.md").write_text(text)
    return tmp_path / "lib"


def test_rev3_heading_uses_title_and_quotes_the_requirement(tmp_path):
    cat = ('id,family,family_code,title,requirement\n'
           '03.01.01,Access Control,AC,Account Management,"a. Define the types.\nb. Create accounts."\n')
    blk = "<!-- chp:control id=03.01.01 status=pending evidence= -->\n**Implementation:** Pending.\n"
    ssp = assemble(lib(tmp_path, cat, {"03.01.01": blk}))["ssp.md"]
    assert "#### 03.01.01 Account Management\n\n> a\\. Define the types.\\\n> b\\. Create accounts.\n\n" in ssp


def test_rev2_heading_is_unchanged(tmp_path):
    cat = "id,family,family_code,basic_derived,requirement\n3.1.1,Access Control,AC,Basic,Limit access.\n"
    blk = "<!-- chp:control id=3.1.1 status=site evidence= -->\n**Implementation:** None.\n"
    ssp = assemble(lib(tmp_path, cat, {"3.1.1": blk}))["ssp.md"]
    assert "#### 3.1.1 Limit access.\n\n**Status:** site." in ssp and "> " not in ssp


def test_pending_status_line_says_not_yet_proven():
    line = _status_line("<!-- chp:control id=03.01.01 status=pending evidence= -->\nx")
    assert line == ("**Status:** pending (not yet proven on the Rev 3 reference implementation). "
                    "**Evidence:** none yet.\n\n")


def test_odp_defaults_load_and_are_marked_as_defaults(tmp_path):
    d = tmp_path / "defaults.ini"
    d.write_text("[odp]\n03_01_01_f_02 = at most 90 days\n[other]\nx = 1\n")
    v, _, prov = load_values(None, None, d, MAP)
    assert v["odp.03_01_01_f_02"] == "at most 90 days" and prov["odp.03_01_01_f_02"] == DEFAULT
    assert "other.x" not in v


def test_profile_overrides_an_odp_default(tmp_path):
    d = tmp_path / "defaults.ini"
    d.write_text("[odp]\n03_01_01_f_02 = at most 90 days\n")
    p = tmp_path / "p.ini"
    p.write_text("[odp]\n03_01_01_f_02 = 30 days\n")
    v, _, prov = load_values(p, None, d, MAP)
    assert v["odp.03_01_01_f_02"] == "30 days" and prov["odp.03_01_01_f_02"] == "profile"


def test_rev3_quoted_numbered_lines_stay_one_paragraph(tmp_path):
    # final review I2: "> 1. ..." would start a CommonMark list and swallow the next lettered part
    cat = ('id,family,family_code,title,requirement\n'
           '03.01.01,Access Control,AC,Account Management,"c. Specify:\n1. Authorized users,\nd. Authorize access."\n')
    blk = "<!-- chp:control id=03.01.01 status=pending evidence= -->\n**Implementation:** Pending.\n"
    ssp = assemble(lib(tmp_path, cat, {"03.01.01": blk}))["ssp.md"]
    assert "> c\\. Specify:\\\n> 1\\. Authorized users,\\\n> d\\. Authorize access.\n" in ssp
