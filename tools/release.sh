#!/usr/bin/env bash
# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
# V=X.Y.Z tools/release.sh (RUNS ON THE MAC, YubiKey plugged in): publish the tagged release templates-V to the For Jeff
# share as chp-templates/V/: the tarball (git archive of the tag), SHA256SUMS and SHA256SUMS.asc signed by the project
# key. Built in <target>.partial; renamed only when every check passed. Never overwrites a published release.
set -Eeuo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; top="$(cd "$here/.." && pwd)"
V=${V:?set V (e.g. 1.0.0)}
FPR=2DE0D71BF37D8F5E4201A590521276F43C908F8E
SHARE="/Volumes/For Jeff"; B="$SHARE/chp-templates"; T="$B/$V"; P="$T.partial"
[[ -d $SHARE ]] || { echo "refusing: $SHARE is not mounted"; exit 1; }
[[ -e $T ]] && { echo "refusing: $T already exists"; exit 1; }
git -C "$top" rev-parse -q --verify "refs/tags/templates-$V" >/dev/null || { echo "refusing: tag templates-$V not found"; exit 1; }
[[ -z $(git -C "$top" status --porcelain) ]] || { echo "refusing: the working tree has uncommitted changes"; exit 1; }
gpg --card-status >/dev/null 2>&1 || { echo "refusing: YubiKey not found (plug it in)"; exit 1; }
echo "== every library's MANIFEST.json must match its files (tools/build_manifest.py verify)"
(cd "$top" && python3 -c 'import sys; sys.path.insert(0,"."); from tools.build_manifest import verify
bad = [p for lib in ("rev2",) for p in verify(lib)]
print("\n".join(bad)); sys.exit(1 if bad else 0)') || { echo "refusing: a manifest is stale"; exit 1; }
mkdir -p "$B"; rm -rf "$P"; mkdir -p "$P"
echo "== tarball from tag templates-$V"
git -C "$top" archive --format=tar.gz --prefix="chp-templates-$V/" -o "$P/chp-templates-$V.tar.gz" "templates-$V"
(cd "$P" && shasum -a 256 "chp-templates-$V.tar.gz" > SHA256SUMS)
echo "== signing SHA256SUMS: a PIN window only if the PIN is not cached (click inside it first), then TOUCH the key"
gpg --local-user "$FPR" --armor --detach-sign -o "$P/SHA256SUMS.asc" "$P/SHA256SUMS"
echo "== checks"
gpg --verify "$P/SHA256SUMS.asc" "$P/SHA256SUMS"
(cd "$P" && shasum -a 256 -c SHA256SUMS)
mv "$P" "$T"
echo "RELEASED: $T"; ls -l "$T"
