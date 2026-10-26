# chp-templates 1.3.0: release notes

**Released:** October 2026 · **Additive; replaces 1.2.0 as current.**

## The Rev 3 library (first batch)

- **NIST SP 800-171 Rev 3 catalog:** 97 requirements in 17 families, from NIST's Rev 2 to Rev 3 change analysis
  (pinned by sha256).
- **Rev 2 → Rev 3 crosswalk** (`rev3/crosswalk.csv`): every Rev 2 ID, its Rev 3 ID(s), and the type of change. NIST's
  workbook labels one withdrawn row "3.11.4", an ID that Rev 2 does not have; that row is skipped, and 3.12.4 maps to
  03.15.02.
- **DoD organization-defined parameters:** the 80 values from DoD's memo signed April 10, 2025. 76 are the library's
  defaults, marked *(default, not yet confirmed)* until a site confirms them. The other 4 are guidance, so the site
  sets them.
- **Every Rev 3 control block is *pending*.** The Rev 3 reference implementation has not yet been assessed, so the
  library does not yet describe the appliance's Rev 3 implementation. Each block names its Rev 2 basis and its
  parameters, and puts the site in charge until the text is written. Narratives come in later releases.
- **A Rev 3 SSP and POA&M,** laid out by the 03.xx families, with the same fixed layouts as Rev 2.

## New placeholders (Automated_Compliance)

- `odp.<part id>`, e.g. `odp.03_01_01_f_02`, in a new `[odp]` section: one per DoD ODP, all public. They are
  separate from the `decision.*` names. Nothing was renamed or removed.

## Rev 2 change

- **POA&M T-06** now says that appliance update 0.2.0-update3 silences the fapolicyd SELinux denials (the access is
  still denied), so a site on that update closes it. Rev 2 content version 1.2.1.

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
