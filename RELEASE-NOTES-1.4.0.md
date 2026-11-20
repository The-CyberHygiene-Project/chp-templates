# chp-templates 1.4.0: release notes

**Released:** November 2026 · **Additive; replaces 1.3.1 as current.** Nothing was renamed or removed, so a profile
that works with 1.3.1 works with 1.4.0.

## Controlled-document templates (new)

The CHP appliance's optional document server (idm-assistant ISO 0.7.0) starts each new controlled document from a
marked template.
- **CUI templates** (`doc/cui/`, Word, Excel and Markdown):
  - The CUI banner is on every page: in Word, the header and footer; in Excel, the sheet's header and footer; in
    Markdown, the first and last lines.
  - The designation block is on page one: in Word, the first-page footer; in Excel, cells A1-A3; in Markdown, after
    the first banner.
  - The block lines are `Controlled by: {{CUI_CONTROLLED_BY}}`, `CUI Category: {{CUI_CATEGORY}}` and
    `POC: {{CUI_POC}}`. The appliance's `chp-site doc new` fills them from the site keys of the same names.
- **Non-CUI twins** (`doc/noncui/`): the same documents, with no CUI marking.
- **Made by `tools/make_doc_templates.py`** (standard library only). The output is byte-reproducible, and a test
  checks that the committed files match it.

## New placeholders and site keys

`site-conf-mapping.csv` maps five new optional `site.conf` keys:

| site.conf key | placeholder | visibility |
|---|---|---|
| `DOC_ISSO_ACCOUNT` | `roles.doc_isso_account` | private |
| `DOC_APPROVER_ACCOUNTS` | `roles.doc_approver_accounts` (list) | private |
| `CUI_CONTROLLED_BY` | `marking.controlled_by` | public |
| `CUI_CATEGORY` | `marking.cui_category` | public |
| `CUI_POC` | `marking.poc` | private |

These are new rows only; the existing rows are unchanged. No SSP or POA&M template uses the new placeholders yet.
`vocabulary.md` also describes the three `{{CUI_*}}` document-template placeholders. They are not `chpfill` names.

## Rev 2 narratives for the document workflow

These requirements now describe the optional document server and its controlled-document workflow (check-out,
approval by someone other than the author, publish, marking, tagging, the document ledger). Rev 2 content version is
**1.2.5** (1.2.4 was 3.8.9's `/backup` volume, from 1.4.0's base branch).

- **3.1.3** (partial):
  - The CUI, FCI and Archive folders cannot be shared. Public links to CUI or FCI are refused. A file leaves CUI
    only for Archive.
  - NextCloud has no internet access.
  - A nightly canary account, `chp-canary`, checks the refusals.
  - **Download and re-upload of CUI** is accepted as an insider risk (owner decision 2). It is recorded in the audit
    log and forbidden by a site rule.
  - **MD5 degraded mode** (FIPS database): moves, renames and deletes of non-empty folders are refused, and the
    server reports DEGRADED.
- **3.1.22** (site): the server is LAN-only. It refuses public links to CUI or FCI and every federated share; any
  other public link needs a password and expires within 7 days. Controlled documents are published only after an
  approval.
- **3.3.1** (partial):
  - Wazuh reads NextCloud's audit log.
  - The document ledger is hash-chained and records only Kanidm-verified identities.
  - Audit records and alert text can carry CUI file names and paths. The records stay on the appliance; the
    text of each alert at or above the site's alert level goes to the site's `ALERT_HOOK`, which the site must keep
    inside the CUI boundary or on a channel authorised for CUI.
- **3.4.3** (partial):
  - Controlled documents change only by check-out, approval and publish.
  - Only root writes the Compliance areas, as the local account `chp-publisher`.
  - The approver is outside the cycle's authors and approves the exact SHA-256.
  - The ISSO override needs a reason.
  - Identity comes only from Kanidm's `chp-doc` userinfo.
  - **Every approval and every override alerts at once** (level 12). The residual risk that a compromised server
    forges an approval with a replayed live token is accepted, with this detection (owner decision 9).
- **3.8.4** (now partial; was site): marked templates, filled from the marking site keys; the marking check on the
  workstation and again on the server; tagging on arrival, with a nightly tag check.
- **3.8.9** (now partial; was site): the document server's nightly backup goes into the encrypted `/backup` volume.
- **3.13.8** (appliance): the document server is HTTPS on the LAN only, with a site-CA certificate. Workstation
  commands and token checks are pinned to the site root.
- **Evidence:** the narratives add the idm-assistant proof record `lab/docs-proof/PROOF-RECORD-PLAN2.md` (the
  document server). The workflow's own lab proof follows in a later content version.

The Rev 3 library is unchanged (0.1.0, all *pending*).

## New files (flag for consumers)

- `doc/cui/CUI_Template_v0.1-DRAFT.docx`
- `doc/cui/CUI_Template_v0.1-DRAFT.xlsx`
- `doc/cui/CUI_Template_v0.1-DRAFT.md`
- `doc/noncui/Template_v0.1-DRAFT.docx`
- `doc/noncui/Template_v0.1-DRAFT.xlsx`
- `doc/noncui/Template_v0.1-DRAFT.md`
- `tools/make_doc_templates.py`
- `tests/test_doc_templates.py`
- `RELEASE-NOTES-1.4.0.md`

`.gitignore` gains two lines so the `.docx` templates are tracked (it ignores `*.docx` elsewhere).

## For a site

Regenerate the SSP. If the document server is off (`DOCUMENTS=no`), the narratives still describe it as optional,
and the site responsibility lines cover these requirements.

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
