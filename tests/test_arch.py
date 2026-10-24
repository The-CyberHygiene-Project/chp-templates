import os
import re
from pathlib import Path

import pytest
from render.chpfill import TOKEN, load_vocabulary, vocab_entry

TOP = Path(__file__).resolve().parents[1]
ARCH = (TOP / "rev2/templates/ssp/arch/chp-appliance.md").read_text()
EVIDENCE = re.compile(r"\(evidence: idm-assistant ([^)\s;]+(?:; ?[^)\s;]+)*)\)")
COMPONENTS = ["Kanidm", "step-ca", "SSH certificate authority", "BIND", "kanidm-unixd", "Google Authenticator",
              "USBGuard", "fapolicyd", "LUKS", "TPM", "FIPS", "AIDE", "CHP monitor", "chrony", "SELinux", "site stick"]


def test_names_every_component():
    for c in COMPONENTS:
        assert c in ARCH, c


def test_every_component_bullet_cites_evidence():
    bullets = []
    for line in ARCH.splitlines():           # a bullet plus its indented continuation lines
        if line.startswith("- **"):
            bullets.append(line)
        elif bullets and line.startswith("  ") and line.strip():
            bullets[-1] += " " + line.strip()
    assert len(bullets) >= 12
    for b in bullets:
        assert EVIDENCE.search(b), b


@pytest.mark.skipif(not os.environ.get("IDM_ASSISTANT"), reason="set IDM_ASSISTANT to the idm-assistant checkout")
def test_evidence_paths_exist():
    root = Path(os.environ["IDM_ASSISTANT"])
    for m in EVIDENCE.finditer(ARCH):
        for p in m.group(1).split(";"):
            assert (root / p.strip().split("#")[0]).exists(), p


def test_placeholders_in_vocabulary_and_boundary_list():
    v = load_vocabulary(TOP / "vocabulary.md")
    assert all(vocab_entry(m.group(1), v) for m in TOKEN.finditer(ARCH))
    assert "{{site.domain}}" in ARCH
