import subprocess
import sys
from pathlib import Path

import pytest
from render.chpfill import assemble

TOP = Path(__file__).resolve().parents[1]


def make_lib(tmp_path):
    lib = tmp_path / "lib"
    (lib / "templates/ssp/controls").mkdir(parents=True)
    (lib / "templates/ssp/arch").mkdir()
    (lib / "templates/poam").mkdir()
    (lib / "catalog.csv").write_text(
        "id,family,family_code,basic_derived,requirement\n"
        "3.1.1,Access Control,AC,Basic,Limit access.\n3.1.2,Access Control,AC,Basic,Limit functions.\n"
        "3.2.1,Awareness and Training,AT,Basic,Ensure awareness.\n")
    (lib / "templates/ssp/frame.md").write_text(
        "# SSP for {{organization.name}}\n{{> family_status}}\n{{> arch}}\n## 4. CONTROLS\n{{> controls}}\nEnd {{site.domain}}\n")
    (lib / "templates/ssp/arch/chp-appliance.md").write_text("Arch text.\n")
    for cid in ("3.1.1", "3.1.2", "3.2.1"):
        (lib / f"templates/ssp/controls/{cid}.md").write_text(
            f"<!-- chp:control id={cid} status=site evidence= -->\n**Implementation:** block {cid}.\n")
    (lib / "templates/poam/frame.md").write_text("# POA&M {{organization.name}}\n")
    return lib


def test_assemble_orders_blocks_and_counts_families(tmp_path):
    docs = assemble(make_lib(tmp_path))
    ssp = docs["ssp.md"]
    assert ssp.index("### 4.1 Access Control (AC)") < ssp.index("#### 3.1.1 Limit access.") < ssp.index("#### 3.1.2")
    assert ssp.index("#### 3.1.2") < ssp.index("### 4.2 Awareness and Training (AT)") < ssp.index("#### 3.2.1")
    assert "<!-- chp:control" not in ssp and "Arch text." in ssp
    assert "#### 3.1.1 Limit access.\n\n**Status:** site. **Evidence:** none (the site's responsibility).\n" in ssp
    assert "| AC — Access Control | 2 | {{status.ac.met}} | {{status.ac.not_met}} | {{status.ac.unverified}} |" in ssp
    assert "| **TOTAL** | **3** |" in ssp and docs["poam.md"].startswith("# POA&M")


def run(*args):
    return subprocess.run([sys.executable, str(TOP / "render/chpfill.py"), *map(str, args)], capture_output=True, text=True)


def test_fill_writes_three_files_and_reports(tmp_path):
    lib = make_lib(tmp_path)
    p = tmp_path / "p.ini"
    p.write_text("[organization]\nname = Example Manufacturing LLC\n")
    r = run("fill", "--lib", lib, "--profile", p, "--out", tmp_path / "out", "--vocabulary", TOP / "vocabulary.md")
    assert r.returncode == 0, r.stderr
    out = tmp_path / "out"
    assert sorted(x.name for x in out.iterdir()) == ["fill-report.md", "poam.md", "ssp.md"]
    rep = (out / "fill-report.md").read_text()
    assert "site.domain" in rep and "ssp.md" in rep


def test_fill_error_leaves_nothing(tmp_path):
    lib = make_lib(tmp_path)
    (lib / "templates/poam/frame.md").write_text("{{#if facts.a}}\nno close\n")
    p = tmp_path / "p.ini"
    p.write_text("[organization]\nname = X\n")
    r = run("fill", "--lib", lib, "--profile", p, "--out", tmp_path / "out", "--vocabulary", TOP / "vocabulary.md")
    assert r.returncode == 2 and "templates/poam/frame.md:1: unclosed" in r.stderr
    assert not (tmp_path / "out").exists() and not (tmp_path / "out.partial").exists()


def test_fill_refuses_an_existing_out_dir(tmp_path):
    lib = make_lib(tmp_path)
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "keep.txt").write_text("mine")
    p = tmp_path / "p.ini"
    p.write_text("[organization]\nname = X\n")
    r = run("fill", "--lib", lib, "--profile", p, "--out", tmp_path / "out", "--vocabulary", TOP / "vocabulary.md")
    assert r.returncode == 2 and (tmp_path / "out" / "keep.txt").read_text() == "mine"


def test_status_and_evidence_are_visible(tmp_path):
    lib = make_lib(tmp_path)
    (lib / "templates/ssp/controls/3.1.2.md").write_text(
        "<!-- chp:control id=3.1.2 status=partial evidence=lab/x.md#3;scan:rule_a -->\n**Implementation:** b.\n")
    ssp = assemble(lib)["ssp.md"]
    assert "**Status:** partial. **Evidence:** idm-assistant `lab/x.md#3`; scan rule `rule_a`.\n" in ssp


def test_defaults_are_marked_in_the_document(tmp_path):
    lib = make_lib(tmp_path)
    (lib / "templates/poam/frame.md").write_text("Lockout after {{decision.lockout_threshold}} attempts.\n")
    (lib / "defaults.ini").write_text("[decision]\nlockout_threshold = 3\n")
    p = tmp_path / "p.ini"
    p.write_text("[organization]\nname = X\n")
    r = run("fill", "--lib", lib, "--profile", p, "--out", tmp_path / "out", "--vocabulary", TOP / "vocabulary.md")
    assert r.returncode == 0, r.stderr
    assert "Lockout after 3 *(default, not yet confirmed)* attempts." in (tmp_path / "out/poam.md").read_text()


def test_errors_name_the_source_file(tmp_path):
    lib = make_lib(tmp_path)
    (lib / "templates/ssp/controls/3.1.2.md").write_text(
        "<!-- chp:control id=3.1.2 status=site evidence= -->\n**Implementation:** x.\n{{#if facts.a}}\nno close\n")
    with pytest.raises(Exception, match=r"controls/3\.1\.2\.md:3: unclosed"):
        assemble(lib)


def test_unwritable_output_is_a_clear_error_and_leaves_nothing(tmp_path):
    lib = make_lib(tmp_path)
    ro = tmp_path / "ro"
    ro.mkdir()
    ro.chmod(0o500)
    p = tmp_path / "p.ini"
    p.write_text("[organization]\nname = X\n")
    try:
        r = run("fill", "--lib", lib, "--profile", p, "--out", ro / "out", "--vocabulary", TOP / "vocabulary.md")
    finally:
        ro.chmod(0o700)
    assert r.returncode == 2 and "Traceback" not in r.stderr and not list(ro.iterdir())
