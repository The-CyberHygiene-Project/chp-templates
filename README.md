# chp-templates

Shared **System Security Plan (SSP)** and **Plan of Action and Milestones (POA&M)** templates for NIST SP 800-171,
maintained by the CyberHygiene Project. Two systems use the same library:

- the **CHP Lab Installer's site stick**, which renders a site's SSP and POA&M on the appliance;
- **Automated_Compliance**, which generates the documents and uses them as the canvas a business maintains.

**Placeholder templates only.** No site's values belong in this repository. Every organization, person, host,
address and date is a `{{section.key}}` placeholder, and a test fails the build on anything real.

## Layout

| Path | What it is |
|---|---|
| `rev2/` | the self-contained **Rev 2** library (the CMMC Level 2 basis today): catalog, templates, defaults, manifest |
| `rev3/` | the self-contained **Rev 3** library (Plan C2) |
| `vocabulary.md` | every placeholder: meaning, kind, and visibility (`public`, `private` or `never-to-ai`) |
| `site-conf-mapping.csv` | how a CHP site stick's `site.conf` keys fill placeholders; the other `site.conf` keys are machine settings |
| `render/chpfill.py` | the one renderer (Python 3.9, standard library only) |

## Filling the templates

    python3 render/chpfill.py fill --lib rev2 --profile profile.ini [--site-conf site.conf] --out out/

This writes `ssp.md`, `poam.md` and `fill-report.md`.
- **Unfilled placeholders stay visible** as `{{key}}` and are listed in the report; they are never guessed.
- **Defaults** from `rev2/defaults.ini` are marked *"(default, not yet confirmed)"* until the profile confirms them.
- **`--public`** refuses to place any value tagged private.

To make a Word copy: `pandoc out/ssp.md -o ssp.docx`.

## Releases

Releases are signed tarballs: `chp-templates-X.Y.Z.tar.gz`, `SHA256SUMS` and `SHA256SUMS.asc`. They are signed with the
project release key `2DE0D71BF37D8F5E4201A590521276F43C908F8E`. To check a release, verify the signature, then
`shasum -a 256 -c SHA256SUMS`.

## Licence

Apache License 2.0. NIST requirement text in the catalogs comes from NIST SP 800-171, a US government publication.
