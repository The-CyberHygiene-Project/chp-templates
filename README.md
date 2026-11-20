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
| `rev3/` | the self-contained **Rev 3** library: NIST's Rev 3 catalog, the Rev 2 → Rev 3 crosswalk, the DoD ODP values as defaults; every control block is *pending* until the Rev 3 reference implementation proves it |
| `vocabulary.md` | every placeholder: meaning, kind, and visibility (`public`, `private` or `never-to-ai`) |
| `site-conf-mapping.csv` | how a CHP site stick's `site.conf` keys fill placeholders; the other `site.conf` keys are machine settings |
| `render/chpfill.py` | the one renderer (Python 3.9, standard library only) |
| `doc/` | the controlled-document templates (Word, Excel, Markdown): `cui/` marked for the CUI area, `noncui/` their unmarked twins; made by `tools/make_doc_templates.py` |

## Filling the templates

    python3 render/chpfill.py fill --lib rev2 --profile profile.ini [--site-conf site.conf] --out out/

This writes `ssp.md`, `poam.md` and `fill-report.md`.
Use `--lib rev3` for the Rev 3 plan. Its organization-defined parameters go in profile.ini's `[odp]` section, keyed by the
DoD memo's part ID with dots as underscores (e.g. `03_01_01_f_02`).
- **Unfilled placeholders stay visible** as `{{key}}` and are listed in the report; they are never guessed.
- **Defaults** from `rev2/defaults.ini` are marked *"(default, not yet confirmed)"* until the profile confirms them.
- **`--public`** refuses to place any value tagged private.

To make a Word copy: `pandoc out/ssp.md -o ssp.docx`.

## Document templates

`doc/cui/` holds `CUI_Template_v0.1-DRAFT.docx`, `.xlsx` and `.md`: the CUI banner on every page and the designation
block on page one, with the placeholders `{{CUI_CONTROLLED_BY}}`, `{{CUI_CATEGORY}}` and `{{CUI_POC}}`. `doc/noncui/`
holds `Template_v0.1-DRAFT.*` without any CUI marking. The CHP appliance installs them as
`/usr/share/chp-templates/doc/{cui,noncui}/Template.<ext>`, and `chp-site doc new` fills the placeholders from the site
keys of the same names. They are generated, byte for byte: after a change, run `python3 tools/make_doc_templates.py`
and commit the result.

## Releases

Releases are signed tarballs: `chp-templates-X.Y.Z.tar.gz`, `SHA256SUMS` and `SHA256SUMS.asc`. They are signed with the
project release key `2DE0D71BF37D8F5E4201A590521276F43C908F8E`. To check a release, verify the signature, then
`shasum -a 256 -c SHA256SUMS`.

## Licence

Apache License 2.0. NIST requirement text in the catalogs comes from NIST SP 800-171, a US government publication.
