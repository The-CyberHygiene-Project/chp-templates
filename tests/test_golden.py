import shutil
import subprocess
import sys
from pathlib import Path

import pytest

TOP = Path(__file__).resolve().parents[1]


def render(tmp_path):
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(TOP / "render/chpfill.py"), "fill", "--lib", str(TOP / "rev2"), "--profile",
                        str(TOP / "tests/fixtures/example-profile.ini"), "--out", str(out), "--templates-version", "1.0.0"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return out


def test_golden_render_is_complete_and_matches_the_snapshot(tmp_path):
    out = render(tmp_path)
    assert "- none" in (out / "fill-report.md").read_text().split("## Values filled")[0]
    for name in ("ssp.md", "poam.md", "fill-report.md"):
        assert (out / name).read_text() == (TOP / "tests/golden" / name).read_text(), f"{name} differs from tests/golden"


@pytest.mark.skipif(not shutil.which("pandoc"), reason="pandoc not installed")
def test_word_copy_renders(tmp_path):
    out = render(tmp_path)
    r = subprocess.run(["pandoc", str(out / "ssp.md"), "-o", str(tmp_path / "ssp.docx")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "ssp.docx").stat().st_size > 20_000
