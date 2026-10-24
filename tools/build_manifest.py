# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""build_manifest.py LIB VERSION: write LIB/MANIFEST.json (every library file, its sha256, its placeholders and, for a
control block, its status). verify(LIB) lists every file whose content no longer matches the manifest."""
import hashlib
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"\{\{(?:#if )?([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)")
STATUS = re.compile(r"^<!-- chp:control id=\S+ status=(\w+) ")


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(lib):
    return sorted(p for p in lib.rglob("*") if p.is_file() and p.name != "MANIFEST.json")


def build(lib, version):
    lib = Path(lib)
    files = []
    for p in _files(lib):
        rel = p.relative_to(lib).as_posix()
        text = p.read_text(encoding="utf-8")
        entry = {"path": rel, "sha256": _sha(p), "placeholders": sorted(set(TOKEN.findall(text)))}
        m = STATUS.match(text)
        if m:
            entry["status"] = m.group(1)
        files.append(entry)
    manifest = {"library": lib.name, "content_version": version, "catalog_sha256": _sha(lib / "catalog.csv"),
                "files": files}
    (lib / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def verify(lib):
    lib = Path(lib)
    m = json.loads((lib / "MANIFEST.json").read_text(encoding="utf-8"))
    listed = {f["path"]: f["sha256"] for f in m["files"]}
    problems = []
    for p in _files(lib):
        rel = p.relative_to(lib).as_posix()
        if rel not in listed:
            problems.append(f"{rel}: not in MANIFEST.json")
        elif listed.pop(rel) != _sha(p):
            problems.append(f"{rel}: content differs from MANIFEST.json (re-run tools/build_manifest.py)")
    problems += [f"{rel}: listed in MANIFEST.json but missing" for rel in listed]
    if m.get("catalog_sha256") != _sha(lib / "catalog.csv"):
        problems.append("catalog.csv: catalog_sha256 differs")
    return problems


if __name__ == "__main__":
    out = build(Path(sys.argv[1]), sys.argv[2])
    print(f"wrote {sys.argv[1]}/MANIFEST.json: {len(out['files'])} files, content version {out['content_version']}")
