# PLAN OF ACTION AND MILESTONES (POA&M)

## NIST SP 800-171 Rev 2

**Organization:** {{organization.legal_name}}\
**System:** {{system.name}}\
**Version:** {{document.version}} **Date:** {{document.date}}\
**Companion to:** the System Security Plan for {{system.name}}\
**Classification:** {{document.classification}}

## DOCUMENT CONTROL

| Version | Date | Author | Description |
|:---|:---|:---|:---|
| {{document.version}} | {{document.date}} | {{document.author}} | **Initial issue.** Generated from chp-templates {{templates.version}}, with the appliance's known gaps seeded. |

Add each later revision as a new row **above** the previous one (newest first), using MM/DD/YYYY dates.

## HOW TO USE THIS POA&M

Each item records one requirement that is not fully met: the weakness, the plan to correct it, who owns it, and when it
is due. Review the open items every {{decision.review_cycle_months}} months, and record each status change in Document
Control.

Items marked *"seeded by the template: confirm, adapt or close"* come from the CyberHygiene Project appliance's own
known limits. For each one, the site either confirms it applies, adapts it, or closes it with a stated reason.

## ITEMS

| ID | Revision | Requirement | Weakness | Milestones | Scheduled completion | Owner | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|
| T-01 | Rev 2 | 3.10.4 | The appliance keeps no record of physical access to its hosts. *Seeded by the template: confirm, adapt or close.* | Choose a physical access log (for example a room or rack sign-in log); start using it; review it monthly. | {{poam.due_t01}} | {{roles.security_officer}} | Open |
| T-02 | Rev 2 | 3.13.11, 3.5.10 | The identity server's own cryptography runs outside the FIPS-validated module, although the hosts run in FIPS mode. *Seeded by the template: confirm, adapt or close.* | Record the risk decision (accept or remediate); track the upstream FIPS build option. | {{poam.due_t02}} | {{roles.security_officer}} | Open |
| T-03 | Rev 2 | 3.8.6 | The site stick is not encrypted, yet it holds every host's recovery secrets. *Seeded by the template: confirm, adapt or close.* | Store and transport it under physical safeguards (sealed, locked, accompanied), or encrypt it; record each use. | {{poam.due_t03}} | {{roles.security_officer}} | Open |
| T-04 | Rev 2 | 3.1.10, 3.1.11, 3.13.9 | This version of the appliance configures no session lock, session termination or idle network disconnect. *Seeded by the template: confirm, adapt or close.* | Configure the screen lock ({{decision.screen_lock_minutes}} minutes), session termination and SSH idle timeout on every host; verify each. | {{poam.due_t04}} | {{roles.administrator}} | Open |
| T-05 | Rev 2 | 3.5.6, 3.5.8 | This version of the appliance does not disable inactive accounts or enforce password history. *Seeded by the template: confirm, adapt or close.* | Set the identity server's account and password policy; schedule an inactivity review ({{decision.inactivity_disable_days}} days). | {{poam.due_t05}} | {{roles.administrator}} | Open |
| T-06 | Rev 2 | 3.14.6, 3.4.6 | SELinux denials were logged when fapolicyd looked up local accounts at the identity client's socket. Appliance update 0.2.0-update3 silences them; the access is still denied, and no access is lost. *Seeded by the template: confirm, adapt or close.* | Apply update 0.2.0-update3 and close this item with that reason. | {{poam.due_t06}} | {{roles.administrator}} | Open |
| T-07 | Rev 2 | 3.4.3 | If the site stick is removed before a host's first boot finishes, the first later use of the stick raises one file-integrity alert. *Seeded by the template: confirm, adapt or close.* | Leave the stick in until first boot finishes; accept the one alert with an audited approval if it occurs. | {{poam.due_t07}} | {{roles.security_officer}} | Open |
| T-08 | Rev 2 | 3.13.11 | The document server's database runs in FIPS mode and cannot compute MD5, which NextCloud uses when it moves a folder with files in it, or moves a file with old versions to another team folder. The server refuses those operations (DEGRADED mode) so nothing is left half-moved. A publish of a CUI document is also refused when the current published file has old versions, because its old copy moves to another team folder (Archive). *Seeded by the template: confirm, adapt or close.* | Read "DEGRADED" in `chp-site documents status`; use the guide's file-by-file procedure meanwhile; follow the upstream defect report; when status shows "database MD5: available", close this item. | {{poam.due_t08}} | {{roles.administrator}} | Open |
| T-09 | Rev 2 | 3.4.8 | fapolicyd filesystem marks are off (`FSMARK=0`) because fapolicyd 1.4.3-3 exits about a second after a restart with marks on ("recvmesg failed"), which leaves the host without file-execution checks. With marks off, files that services open in their own mount namespace are not checked. The same exit can follow any restart of fapolicyd, also with marks off: enabling the document server restarts it, proves it, and fails loudly if it is not running. *Seeded by the template: confirm, adapt or close.* | Keep `FSMARK=0`; watch monitor check 80; track the fapolicyd version and repeat the trial when Rocky ships a fixed one. | {{poam.due_t09}} | {{roles.security_officer}} | Open |
| T-10 | Rev 2 | 3.13.11, 3.1.5 | The workstation editor (ONLYOFFICE Desktop Editors) bundles a non-validated TLS stack (Chromium with BoringSSL) that ignores the system's FIPS mode, and its Chromium runs with `--no-sandbox` (the app runs unconfined). Its network features are blocked (workstation egress table, hosts block, removed AI Tools plugin), and the editor opens and saves local files only: `chp-site doc` does the transport with the system OpenSSL. *Seeded by the template: confirm, adapt or close.* | Record the risk decision (accept or remediate); keep the egress table and check 83 working; revisit when the vendor ships a sandboxed or validated build. | {{poam.due_t10}} | {{roles.security_officer}} | Open |
| T-11 | Rev 2 | 3.14.1 | NextCloud 35 on this appliance runs on PHP 8.3, which later NextCloud releases do not support. NextCloud is pinned to a release that does. *Seeded by the template: confirm, adapt or close.* | Plan the move to a newer PHP stream or to Rocky 10, and do it before NextCloud 37 is needed; do not take a NextCloud upgrade that needs a newer PHP before then. | {{poam.due_t11}} | {{roles.administrator}} | Open |
| T-12 | Rev 2 | 3.3.8, 3.3.1, 3.5.10 | NextCloud's audit log records the request address of each line. For the sign-in callback that address carries the single-use OIDC `code` and `state`, so they also reach the Wazuh index. The code is bound to the client secret and to PKCE and expires within minutes, so it cannot be replayed from the log. The log is a CUI-boundary record. *Seeded by the template: confirm, adapt or close.* | Keep the audit log and the Wazuh index on the appliance; ask upstream to omit query strings from the log; close when NextCloud can. | {{poam.due_t12}} | {{roles.security_officer}} | Open |
| T-13 | Rev 2 | 3.3.8, 3.3.2 | The approval ledger is hash-chained and checked at the server, but a compromised NextCloud could replay a live approver token, and anyone with a shell on the server can write false `chp-docs-ledger` lines to the journal (`logger -t`), which can raise false alerts. A false line never hides a real event: the checks trust only the ledger and root's journal lines. Every approval and every ISSO override raises a level-12 alert at once, so a forged or replayed approval is detected, not prevented. *Seeded by the template: confirm, adapt or close.* | Accept the residual with detection; keep `SECURITY_ALERT_LEVEL` at 12 or lower while the document server is on (approvals and overrides are level 12, and above that they reach only the daily summary); deliver `ALERT_HOOK` to someone who reads it the same day; export the ledger head to the site stick (`chp-site doc-ledger export`) and verify it (`chp-site doc-ledger verify --stick`). | {{poam.due_t13}} | {{roles.security_officer}} | Open |
| T-14 | Rev 2 | 3.13.1, 3.1.3 | The workstation's network rules allow DNS to the site resolver, and the resolver forwards upstream. Data could be sent out by encoding it in DNS names (DNS tunnelling). DNS to any other server, DNS over TLS and DNS over QUIC are refused. *Seeded by the template: confirm, adapt or close.* | Record the risk decision; let the site resolver log its queries and review them; consider restricting what the resolver forwards. | {{poam.due_t14}} | {{roles.security_officer}} | Open |
| T-15 | Rev 2 | 3.1.1, 3.5.2 | Three NextCloud accounts live outside Kanidm: `chp-publisher` (the root appender's account, which alone writes the Compliance and Superseded areas, and is in `cui-users`), `chp-canary` (the nightly share test, disabled between runs) and `ncadmin` (the break-glass administrator). The first two have no usable password (the publisher's is reset to a random value that nobody keeps, at every `chp-site documents enable`), so no one can sign in as them. `ncadmin` has a usable password, kept in the site stick's `escrow/` folder; every sign-in as `ncadmin` pages at level 12. *Seeded by the template: confirm, adapt or close.* | Name an owner for all three; check 81 already accepts exactly the publisher and the canary in `cui-users` and flags any other; keep the stick safe; review all three at every access review. | {{poam.due_t15}} | {{roles.administrator}} | Open |
| T-16 | Rev 2 | 3.8.4 | The CUI banner check reads text only: a banner in a white or 1-point font passes. It does not pass when it is missing, in a text box, hidden or deleted text, or in the wrong place. *Seeded by the template: confirm, adapt or close.* | Record the residual; add a visual check to the approver's review of each controlled document. | {{poam.due_t16}} | {{roles.security_officer}} | Open |

Add the site's own items below the seeded ones, numbered P-01, P-02 and so on.

## EVIDENCE FOR THE SEEDED ITEMS

The seeded items come from the appliance's release and proof records. Each item's evidence is named in the System
Security Plan's narrative for the same requirement.
