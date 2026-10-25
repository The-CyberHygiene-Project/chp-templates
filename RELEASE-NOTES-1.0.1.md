# chp-templates 1.0.1: release notes

**Released:** October 2026 · **Supersedes 1.0.0.** Use 1.0.1; 1.0.0 should not be used to generate documents.

## Fixes (from the pre-publication review)

- **Defaults are now marked in the document itself** with *(default, not yet confirmed)*, as the README and
  `defaults.ini` describe. Before, only the fill-in report listed them.
- **A blank value no longer fills a blank.** `key =` in `profile.ini`, or a blank `site.conf` line such as
  `ISSO_NAME=`, now leaves the placeholder visible and lists it in the fill-in report.
- **Errors name the file a person edits**, for example `templates/ssp/controls/3.1.2.md:3`, not a line in the
  assembled document.
- **A profile that is not UTF-8, or an output folder that cannot be written, gives a clear error** instead of a
  traceback, and leaves no partial output.

## Narrative corrections

- **3.1.8 states the values the appliance enforces:** lockout after 3 failed attempts within 15 minutes, until an
  administrator unlocks the account. A site's profile can no longer change an "appliance" sentence; a test enforces
  this for every appliance-status requirement.
- **3.5.3 names all four local accounts exempt from the second factor.** They are the root console, `chpadmin`
  (break-glass), and `diag` and `chpcache` (single-command SSH service keys).
- **3.3.8 no longer claims audit logs are readable by root only**, because no passing scan rule proves it.
- **3.13.8 now gives the site the job of protecting CUI sent by email, web or file transfer from workstations.**

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
