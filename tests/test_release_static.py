from pathlib import Path

T = (Path(__file__).resolve().parents[1] / "tools" / "release.sh").read_text()


def test_release_script_contract():
    assert "set -Eeuo pipefail" in T and 'V=${V:?' in T
    assert 'T="$B/$V"' in T and '[[ -e $T ]] && { echo "refusing:' in T            # never overwrites a release
    assert "git archive" in T and "templates-$V" in T and "chp-templates-$V.tar.gz" in T
    assert "--armor --detach-sign" in T and "2DE0D71BF37D8F5E4201A590521276F43C908F8E" in T
    assert "gpg --verify" in T and "shasum -a 256 -c SHA256SUMS" in T
    assert '.partial' in T and 'mv "$P" "$T"' in T
    assert "verify(" in T or "build_manifest" in T                                   # the manifest is checked first


def test_release_checks_every_library_manifest():
    assert 'for lib in ("rev2", "rev3")' in T
