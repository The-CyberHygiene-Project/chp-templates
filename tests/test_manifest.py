import json
import shutil
from pathlib import Path

from tools.build_manifest import build, verify

TOP = Path(__file__).resolve().parents[1]
LIB = TOP / "rev2"


def test_manifest_matches_the_library():
    m = json.loads((LIB / "MANIFEST.json").read_text())
    assert m["library"] == "rev2" and m["content_version"] and len(m["catalog_sha256"]) == 64
    assert verify(LIB) == []
    paths = {f["path"] for f in m["files"]}
    assert "templates/ssp/frame.md" in paths and "templates/poam/frame.md" in paths
    assert sum(p.startswith("templates/ssp/controls/") for p in paths) == 110


def test_manifest_detects_a_stale_file(tmp_path):
    copy = tmp_path / "rev2"
    shutil.copytree(LIB, copy)
    (copy / "templates/ssp/controls/3.1.1.md").write_text("changed\n")
    problems = verify(copy)
    assert problems and "templates/ssp/controls/3.1.1.md" in problems[0]


def test_build_is_deterministic(tmp_path):
    copy = tmp_path / "rev2"
    shutil.copytree(LIB, copy)
    build(copy, json.loads((LIB / "MANIFEST.json").read_text())["content_version"])
    assert (copy / "MANIFEST.json").read_text() == (LIB / "MANIFEST.json").read_text()


def test_rev3_manifest_matches_its_library():
    lib = TOP / "rev3"
    m = json.loads((lib / "MANIFEST.json").read_text())
    assert m["library"] == "rev3" and m["content_version"] == "0.1.0" and verify(lib) == []
    ctrl = [f for f in m["files"] if f["path"].startswith("templates/ssp/controls/")]
    assert len(ctrl) == 97 and {f["status"] for f in ctrl} == {"pending"}


def test_rev2_content_version_moved_for_t06():
    assert json.loads((LIB / "MANIFEST.json").read_text())["content_version"] == "1.2.1"
