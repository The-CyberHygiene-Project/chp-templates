# Vocabulary: every placeholder the templates may use

This is the shared contract for both consumers.
- **Placeholders are only ever added.** A placeholder is never renamed or removed; at most it is marked deprecated, with
  its replacement named.
- **A pattern segment** written `<n>` (a number) or `<name>` (a short lowercase name) matches one entry per item, as in
  `contract.<n>.label`.
- **Kind** is one of:
  - `value`: a single value;
  - `list`: one item per line in `profile.ini`;
  - `fact`: yes or no, used in `{{#if}}` blocks.
- **Visibility** is one of:
  - `public`: may appear in a published copy;
  - `private`: refused by `--public`;
  - `never-to-ai`: refused by `--public`, and never sent to an AI tool.

| placeholder | kind | visibility | meaning |
|---|---|---|---|
| `organization.name` | value | public | the organization's common name |
| `organization.legal_name` | value | public | the legal entity name |
| `organization.dba` | value | public | the trading name, if different |
| `organization.location` | value | public | city and state, public form only |
| `roles.system_owner` | value | private | the person accountable for the system |
| `roles.security_officer` | value | private | the ISSO (from `site.conf` ISSO_NAME) |
| `roles.administrator` | value | private | the system administrator |
| `roles.approver_of_changes` | value | private | who approves changes to the system |
| `roles.baseline_delegates` | list | private | people besides the ISSO who may accept file-integrity baselines (from `site.conf` BASELINE_DELEGATES) |
| `scope.cui_types` | list | public | the categories of CUI the system handles |
| `scope.boundary_note` | value | public | a short statement of what is inside the boundary |
| `site.domain` | value | public | the site's DNS domain (from `site.conf` DOMAIN) |
| `site.lan_subnet` | value | private | the site network (from `site.conf` SUBNET) |
| `site.lan_gateway` | value | private | the site gateway (from `site.conf` GATEWAY) |
| `site.timezone` | value | public | the site's time zone (from `site.conf` TIMEZONE) |
| `contract.<n>.label` | value | private | a short label for contract n |
| `status.<name>.met` | value | private | requirements met in a family (or `total`), from the site's assessment |
| `status.<name>.not_met` | value | private | requirements not met in a family (or `total`) |
| `status.<name>.unverified` | value | private | requirements not yet verified in a family (or `total`) |
| `organization.uei` | value | private | the Unique Entity ID (SAM.gov) |
| `organization.cage` | value | private | the CAGE code |
| `organization.owner_email` | value | private | the System Owner's email address |
| `system.name` | value | public | the system's name, as used throughout the plan |
| `system.purpose` | value | public | what the system is for, in a short paragraph |
| `system.status` | value | public | operational status (e.g. operational, under development) |
| `system.appliance_version` | value | public | the installed CyberHygiene Project appliance version |
| `systems.in_boundary` | list | private | the systems inside the boundary, one per line |
| `document.version` | value | public | this plan's version |
| `document.date` | value | public | this plan's date (MM/DD/YYYY) |
| `document.author` | value | private | who issued this version |
| `document.classification` | value | public | the document's classification marking |
| `document.status` | value | public | the document's approval status |
| `document.next_review` | value | public | the next scheduled review date |
| `assessment.sprs_score` | value | private | the SPRS score; never filled from a template |
| `assessment.sprs_basis` | value | private | who assessed, when, and under which evidence rule |
| `assessment.sprs_date` | value | private | when the SPRS score was assessed |
| `assessment.objectives_met` | value | private | requirements with every 800-171A objective met |
| `assessment.objectives_date` | value | private | when the objective count was assessed |
| `assessment.strengths` | list | private | key strengths, one per line |
| `assessment.deficits` | list | private | outstanding deficits, one per line (each a POA&M item) |
| `assessment.conclusion` | value | private | the plan's concluding statement |
| `poam.reference` | value | public | the companion POA&M's file name and version |
| `contract.list` | list | private | the contracts in scope, one per line |
| `policies.list` | list | public | the policy and procedure documents this plan relies on |
| `supporting.documents` | list | private | supporting documents and where they are kept |
| `facts.has_outside_it_provider` | fact | public | an outside IT provider has access to the system |
| `decision.review_cycle_months` | value | public | how often the plan and POA&M are reviewed (months) |
| `decision.backup_frequency` | value | public | how often backups are taken |
| `decision.restore_test_frequency` | value | public | how often a restore is tested |
| `decision.lockout_threshold` | value | public | failed logon attempts before lockout |
| `decision.lockout_minutes` | value | public | lockout duration (minutes) |
| `decision.password_min_length` | value | public | minimum password length |
| `decision.password_history` | value | public | passwords remembered (no reuse) |
| `decision.inactivity_disable_days` | value | public | days of inactivity before an account is disabled |
| `decision.screen_lock_minutes` | value | public | idle minutes before the screen locks |
| `decision.audit_retention_days` | value | public | audit log retention (days) |
| `decision.patch_cadence` | value | public | routine patch cadence |
| `decision.critical_patch_hours` | value | public | hours to apply a critical patch from detection |
| `decision.incident_report_hours` | value | public | hours to report an incident externally |
| `poam.due_t01` | value | private | scheduled completion date for seeded POA&M item T-01 |
| `poam.due_t02` | value | private | scheduled completion date for seeded POA&M item T-02 |
| `poam.due_t03` | value | private | scheduled completion date for seeded POA&M item T-03 |
| `poam.due_t04` | value | private | scheduled completion date for seeded POA&M item T-04 |
| `poam.due_t05` | value | private | scheduled completion date for seeded POA&M item T-05 |
| `poam.due_t06` | value | private | scheduled completion date for seeded POA&M item T-06 |
| `poam.due_t07` | value | private | scheduled completion date for seeded POA&M item T-07 |
| `templates.version` | value | public | the chp-templates release the document was generated from |
