# chp-templates 1.0.0: release notes

**Released:** October 2026 · **First release.**

## What's in it

- **The Rev 2 library (`rev2/`)**, the CMMC Level 2 basis today:
  - a System Security Plan (SSP) and a Plan of Action and Milestones (POA&M) for the CyberHygiene Project appliance;
  - the NIST SP 800-171 Rev 2 catalog, imported from NIST's CSV and pinned by sha256;
  - **110 requirement narratives.** Each is marked *appliance*, *partial* or *site*, and each appliance claim cites
    the appliance's proof records or its passing compliance-scan rules. Totals: 16 appliance, 46 partial, 48 site.
  - **A seeded POA&M** with seven known appliance gaps, each marked "confirm, adapt or close";
  - **defaults only for values the appliance enforces:** account lockout and the minimum local password length.
- **`render/chpfill.py`**, the one renderer for both the installer and Automated_Compliance.
  - It uses only the Python 3.9 standard library.
  - Fill is single pass, and unfilled placeholders stay visible in a fill-in report.
  - It has a `--public` mode, and it refuses secrets in a profile.
- **`vocabulary.md`**: every placeholder, with its meaning and visibility (public, private or never-to-ai).
- **`site-conf-mapping.csv`**: which CHP site-stick `site.conf` keys fill which placeholders.

## Known limits

- **The narratives describe CHP appliance version 0.2.0.** Session lock, session timeouts, inactivity disable,
  password history, antivirus and network intrusion detection are not in that version, so those requirements are the
  site's until a later appliance release adds them.
- **There is no Rev 3 library yet** (Plan C2).
- **One architecture only:** the CHP appliance (RS#3).

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
