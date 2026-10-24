"""Nothing real in the library: placeholders only (spec §6). Test files and fixtures are excluded (made-up values)."""
import re
import subprocess
from pathlib import Path

TOP = Path(__file__).resolve().parents[1]
ALLOWED_DOMAINS = {"example.test", "csrc.nist.gov", "nist.gov", "doi.org", "www.apache.org", "apache.org", "sam.gov", "checklists.nist.gov"}
DENY = re.compile(r"(?i)cyberinabox|diwai|contract-coach|shannon|PRIVATE KEY")
IPV4 = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b")
EMAIL = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
DOMAIN = re.compile(r"(?i)\b((?:[a-z0-9-]+\.)+(?:com|net|org|gov|mil|edu|io|us|tech|info|biz))\b")


def files():
    out = subprocess.run(["git", "ls-files"], cwd=TOP, capture_output=True, text=True).stdout.split()
    return [TOP / f for f in out if not f.startswith("tests/") and f != "LICENSE"]


def test_no_real_names_addresses_or_keys():
    bad = []
    for p in files():
        t = p.read_text(encoding="utf-8", errors="replace")
        rel = p.relative_to(TOP)
        bad += [f"{rel}: {m.group(0)}" for m in DENY.finditer(t)]
        bad += [f"{rel}: {m.group(1)}" for m in IPV4.finditer(t)
                if not m.group(1).startswith(("192.0.2.", "127.0.0.1", "0.0.0.0"))]
        bad += [f"{rel}: {m.group(0)}" for m in EMAIL.finditer(t) if m.group(1) != "example.test"]
        bad += [f"{rel}: {m.group(1)}" for m in DOMAIN.finditer(t) if m.group(1).lower() not in ALLOWED_DOMAINS]
    assert bad == []
