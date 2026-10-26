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
| `contract.<n>.label` | value | private | a short label for contract n (Automated_Compliance's committed name) |
| `contract.<n>.agency_group` | value | private | the agency or customer group (Automated_Compliance's committed name) |
| `contract.<n>.vehicle` | value | private | the contract vehicle (prime contract, purchase order, subcontract) (Automated_Compliance's committed name) |
| `contract.<n>.information` | value | private | the kind of information the contract involves (Automated_Compliance's committed name) |
| `contract.<n>.clauses` | value | private | the governing clauses, for example DFARS 252.204-7012 (Automated_Compliance's committed name) |
| `contract.<n>.required_revision` | value | private | the NIST SP 800-171 revision the contract requires (Automated_Compliance's committed name) |
| `contract.<n>.revision_basis` | value | private | why that revision applies (clause, letter, deviation) (Automated_Compliance's committed name) |
| `contract.<n>.last_verified` | value | private | when the contract's requirements were last checked (Automated_Compliance's committed name) |
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
| `systems.in_boundary` | list | private | the systems inside the boundary. **Derived** by the renderer from every `system.<name>` whose `in_boundary` is yes. Setting it directly is **deprecated** (still accepted when no `system.<name>` entries exist) |
| `system.<name>.kind` | value | private | what the system is (for example identity server, workstation) |
| `system.<name>.in_boundary` | value | private | yes or no: the system is inside the CUI boundary |
| `system.<name>.operating_system` | value | private | the system's operating system |
| `system.<name>.administered_by` | value | private | who administers the system |
| `system.<name>.provider` | value | private | the outside provider that supplies or manages it, if any |
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
| `contract.list` | list | private | the contracts in scope. **Derived** by the renderer from the `contract.<n>` entries ("label (clauses)", in number order). Setting it directly is **deprecated** (still accepted when no `contract.<n>` entries exist) |
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

## Reserved names (Automated_Compliance draft, 2026-10-25)

These names come from Automated_Compliance's draft vocabulary. They are reserved under the same names, so the two systems never diverge. A profile may set them, but no template uses them yet. A template adopts one only when a section needs it, and that release says so.

| placeholder | kind | visibility | meaning |
|---|---|---|---|
| `decision.log_review_frequency` | value | public | RESERVED (Automated_Compliance draft): how often audit logs are reviewed |
| `decision.alert_notify_minutes` | value | public | RESERVED (Automated_Compliance draft): minutes within which an alert is seen by a person |
| `decision.incident_internal_notify_hours` | value | public | RESERVED (Automated_Compliance draft): hours to notify internally of an incident |
| `decision.incident_contain_hours` | value | public | RESERVED (Automated_Compliance draft): hours to contain an incident |
| `decision.incident_recover_hours` | value | public | RESERVED (Automated_Compliance draft): hours to recover from an incident |
| `decision.visitor_log_required` | value | public | RESERVED (Automated_Compliance draft): yes or no: a visitor log is kept |
| `facts.has_mail_service` | fact | public | RESERVED (Automated_Compliance draft): the system runs a mail service |
| `facts.has_nas` | fact | public | RESERVED (Automated_Compliance draft): network-attached storage is in the boundary |
| `facts.has_remote_access` | fact | public | RESERVED (Automated_Compliance draft): remote access into the boundary is allowed |
| `facts.has_wireless` | fact | public | RESERVED (Automated_Compliance draft): wireless networking reaches the boundary |
| `facts.has_mobile_devices` | fact | public | RESERVED (Automated_Compliance draft): mobile devices connect to the system |
| `facts.uses_local_ai` | fact | public | RESERVED (Automated_Compliance draft): a locally hosted AI tool is used with system data |
| `facts.uses_external_ai` | fact | public | RESERVED (Automated_Compliance draft): an external AI service is used with system data |
| `facts.has_removable_media` | fact | public | RESERVED (Automated_Compliance draft): removable media are used with CUI |
| `facts.has_public_services` | fact | public | RESERVED (Automated_Compliance draft): the system publishes services to the internet |
| `organization.owner_name` | value | private | RESERVED (Automated_Compliance draft): the owner's name |
| `site.directory_base` | value | public | RESERVED (Automated_Compliance draft): the directory base name derived from the domain |
| `site.admin_account` | value | private | RESERVED (Automated_Compliance draft): the site administrator's account name |
| `site.admin_email` | value | private | RESERVED (Automated_Compliance draft): the site administrator's email address |
| `site.host.<name>.address` | value | private | RESERVED (Automated_Compliance draft): a host's network address |
| `site.host.<name>.role` | value | private | RESERVED (Automated_Compliance draft): a host's role |
| `site.wan.<name>.address` | value | private | RESERVED (Automated_Compliance draft): a public address, by service |
| `site.hostname.<name>` | value | private | RESERVED (Automated_Compliance draft): a service's host name, built from the domain |

<!-- odp:begin (generated by tools/odp_tables.py; do not edit) -->

Rev 3 organization-defined parameters. The key is the DoD memo's part ID with the dots written
as underscores. The DoD value is the Rev 3 library's default (`rev3/defaults.ini`).

| placeholder | kind | visibility | meaning |
|---|---|---|---|
| `odp.03_01_01_f_02` | value | public | DoD ODP 03.01.01.f.02 (Rev 3 03.01.01): [Assignment: organization-defined time period] |
| `odp.03_01_01_g_01` | value | public | DoD ODP 03.01.01.g.01 (Rev 3 03.01.01): [Assignment: organization-defined time period] |
| `odp.03_01_01_g_02` | value | public | DoD ODP 03.01.01.g.02 (Rev 3 03.01.01): [Assignment: organization-defined time period] |
| `odp.03_01_01_g_03` | value | public | DoD ODP 03.01.01.g.03 (Rev 3 03.01.01): [Assignment: organization-defined time period] |
| `odp.03_01_01_h_01` | value | public | DoD ODP 03.01.01.h.01 (Rev 3 03.01.01): [Assignment: organization-defined time period] |
| `odp.03_01_01_h_02` | value | public | DoD ODP 03.01.01.h.02 (Rev 3 03.01.01): [Assignment: organization-defined circumstances] |
| `odp.03_01_05_b_01` | value | public | DoD ODP 03.01.05.b.01 (Rev 3 03.01.05): [Assignment: organization-defined security functions] |
| `odp.03_01_05_b_02` | value | public | DoD ODP 03.01.05.b.02 (Rev 3 03.01.05): [Assignment: organization-defined security-relevant information] |
| `odp.03_01_05_c` | value | public | DoD ODP 03.01.05.c (Rev 3 03.01.05): [Assignment: organization-defined frequency] |
| `odp.03_01_06_a` | value | public | DoD ODP 03.01.06.a (Rev 3 03.01.06): [Assignment: organization-defined personnel or roles] |
| `odp.03_01_08_a_01` | value | public | DoD ODP 03.01.08.a.01 (Rev 3 03.01.08): [Assignment: organization-defined number] |
| `odp.03_01_08_a_02` | value | public | DoD ODP 03.01.08.a.02 (Rev 3 03.01.08): [Assignment: organization-defined time period] |
| `odp.03_01_08_b` | value | public | DoD ODP 03.01.08.b (Rev 3 03.01.08): [Assignment: organization-defined time period] |
| `odp.03_01_10_a` | value | public | DoD ODP 03.01.10.a (Rev 3 03.01.10): [Assignment: organization-defined time period] |
| `odp.03_01_11` | value | public | DoD ODP 03.01.11 (Rev 3 03.01.11): [Assignment: organization-defined conditions or trigger events requiring session disconnect] |
| `odp.03_01_20_b` | value | public | DoD ODP 03.01.20.b (Rev 3 03.01.20): [Assignment: organization-defined security requirements] |
| `odp.03_02_01_a_01` | value | public | DoD ODP 03.02.01.a.01 (Rev 3 03.02.01): [Assignment: organization-defined frequency] |
| `odp.03_02_01_a_02` | value | public | DoD ODP 03.02.01.a.02 (Rev 3 03.02.01): [Assignment: organization-defined events] |
| `odp.03_02_01_b_01` | value | public | DoD ODP 03.02.01.b.01 (Rev 3 03.02.01): [Assignment: organization-defined frequency] |
| `odp.03_02_01_b_02` | value | public | DoD ODP 03.02.01.b.02 (Rev 3 03.02.01): [Assignment: organization-defined events] |
| `odp.03_02_02_a_01` | value | public | DoD ODP 03.02.02.a.01 (Rev 3 03.02.02): [Assignment: organization-defined frequency] |
| `odp.03_02_02_a_02` | value | public | DoD ODP 03.02.02.a.02 (Rev 3 03.02.02): [Assignment: organization-defined events] |
| `odp.03_02_02_b_01` | value | public | DoD ODP 03.02.02.b.01 (Rev 3 03.02.02): [Assignment: organization-defined frequency] |
| `odp.03_02_02_b_02` | value | public | DoD ODP 03.02.02.b.02 (Rev 3 03.02.02): [Assignment: organization-defined events] |
| `odp.03_03_01_a` | value | public | DoD ODP 03.03.01.a (Rev 3 03.03.01): [Assignment: organization-defined event types] |
| `odp.03_03_01_b` | value | public | DoD ODP 03.03.01.b (Rev 3 03.03.01): [Assignment: organization-defined frequency] |
| `odp.03_03_04_a` | value | public | DoD ODP 03.03.04.a (Rev 3 03.03.04): [Assignment: organization-defined time period] |
| `odp.03_03_04_b` | value | public | DoD ODP 03.03.04.b (Rev 3 03.03.04): [Assignment: organization-defined additional actions] |
| `odp.03_03_05_a` | value | public | DoD ODP 03.03.05.a (Rev 3 03.03.05): [Assignment: organization-defined frequency] |
| `odp.03_03_07_b` | value | public | DoD ODP 03.03.07.b (Rev 3 03.03.07): [Assignment: organization-defined granularity of time measurement] |
| `odp.03_04_01_b` | value | public | DoD ODP 03.04.01.b (Rev 3 03.04.01): [Assignment: organization-defined frequency] |
| `odp.03_04_02_a` | value | public | DoD ODP 03.04.02.a (Rev 3 03.04.02): [Assignment: organization-defined configuration settings] |
| `odp.03_04_06_b` | value | public | DoD ODP 03.04.06.b (Rev 3 03.04.06): [Assignment: organization-defined functions, ports, protocols, connections, and services] |
| `odp.03_04_06_c` | value | public | DoD ODP 03.04.06.c (Rev 3 03.04.06): [Assignment: organization-defined frequency] |
| `odp.03_04_08_c` | value | public | DoD ODP 03.04.08.c (Rev 3 03.04.08): [Assignment: organization-defined frequency] |
| `odp.03_04_10_b` | value | public | DoD ODP 03.04.10.b (Rev 3 03.04.10): [Assignment: organization-defined frequency] |
| `odp.03_04_12_a` | value | public | DoD ODP 03.04.12.a (Rev 3 03.04.12): [Assignment: organization-defined system configurations] |
| `odp.03_04_12_b` | value | public | DoD ODP 03.04.12.b (Rev 3 03.04.12): [Assignment: organization-defined security requirements] |
| `odp.03_05_01_b` | value | public | DoD ODP 03.05.01.b (Rev 3 03.05.01): [Assignment: organization-defined circumstances or situations requiring re-authentication] |
| `odp.03_05_02` | value | public | DoD ODP 03.05.02 (Rev 3 03.05.02): [Assignment: organization-defined devices or types of devices] |
| `odp.03_05_05_c` | value | public | DoD ODP 03.05.05.c (Rev 3 03.05.05): [Assignment: organization-defined time period] |
| `odp.03_05_05_d` | value | public | DoD ODP 03.05.05.d (Rev 3 03.05.05): [Assignment: organization-defined characteristic identifying individual status] |
| `odp.03_05_07_a` | value | public | DoD ODP 03.05.07.a (Rev 3 03.05.07): [Assignment: organization-defined frequency] |
| `odp.03_05_07_f` | value | public | DoD ODP 03.05.07.f (Rev 3 03.05.07): [Assignment: organization-defined composition and complexity rules] |
| `odp.03_05_12_e_01` | value | public | DoD ODP 03.05.12.e.01 (Rev 3 03.05.12): [Assignment: organization-defined frequency] |
| `odp.03_05_12_e_02` | value | public | DoD ODP 03.05.12.e.02 (Rev 3 03.05.12): [Assignment: organization-defined events] |
| `odp.03_06_02_b` | value | public | DoD ODP 03.06.02.b (Rev 3 03.06.02): [Assignment: organization-defined time period] |
| `odp.03_06_02_c` | value | public | DoD ODP 03.06.02.c (Rev 3 03.06.02): [Assignment: organization-defined authorities] |
| `odp.03_06_03` | value | public | DoD ODP 03.06.03 (Rev 3 03.06.03): [Assignment: organization-defined frequency] |
| `odp.03_06_04_a_01` | value | public | DoD ODP 03.06.04.a.01 (Rev 3 03.06.04): [Assignment: organization-defined time period] |
| `odp.03_06_04_a_03` | value | public | DoD ODP 03.06.04.a.03 (Rev 3 03.06.04): [Assignment: organization-defined frequency] |
| `odp.03_06_04_b_01` | value | public | DoD ODP 03.06.04.b.01 (Rev 3 03.06.04): [Assignment: organization-defined frequency] |
| `odp.03_06_04_b_02` | value | public | DoD ODP 03.06.04.b.02 (Rev 3 03.06.04): [Assignment: organization-defined events] |
| `odp.03_08_07_a` | value | public | DoD ODP 03.08.07.a (Rev 3 03.08.07): [Assignment: organization-defined types of system media] |
| `odp.03_09_01_b` | value | public | DoD ODP 03.09.01.b (Rev 3 03.09.01): [Assignment: organization-defined conditions requiring rescreening] |
| `odp.03_09_02_a_01` | value | public | DoD ODP 03.09.02.a.01 (Rev 3 03.09.02): [Assignment: organization-defined time period] |
| `odp.03_10_01_c` | value | public | DoD ODP 03.10.01.c (Rev 3 03.10.01): [Assignment: organization-defined frequency] |
| `odp.03_10_02_b_01` | value | public | DoD ODP 03.10.02.b.01 (Rev 3 03.10.02): [Assignment: organization-defined frequency] |
| `odp.03_10_02_b_02` | value | public | DoD ODP 03.10.02.b.02 (Rev 3 03.10.02): [Assignment: organization-defined events or potential indications of events] |
| `odp.03_10_06_b` | value | public | DoD ODP 03.10.06.b (Rev 3 03.10.06): [Assignment: organization-defined security requirements] |
| `odp.03_11_01_b` | value | public | DoD ODP 03.11.01.b (Rev 3 03.11.01): [Assignment: organization-defined frequency] |
| `odp.03_11_02_a` | value | public | DoD ODP 03.11.02.a (Rev 3 03.11.02): [Assignment: organization-defined frequency] |
| `odp.03_11_02_b` | value | public | DoD ODP 03.11.02.b (Rev 3 03.11.02): [Assignment: organization-defined response times] |
| `odp.03_11_02_c` | value | public | DoD ODP 03.11.02.c (Rev 3 03.11.02): [Assignment: organization-defined frequency] |
| `odp.03_12_01` | value | public | DoD ODP 03.12.01 (Rev 3 03.12.01): [Assignment: organization-defined frequency] |
| `odp.03_12_05_a` | value | public | DoD ODP 03.12.05.a (Rev 3 03.12.05): [Selection (one or more): interconnection security agreements; information exchange security agreements; memoranda of understanding or agreement; service-level agreements; user agreements; nondisclosure agreements; other types of agreements] |
| `odp.03_12_05_c` | value | public | DoD ODP 03.12.05.c (Rev 3 03.12.05): [Assignment: organization-defined frequency] |
| `odp.03_13_09` | value | public | DoD ODP 03.13.09 (Rev 3 03.13.09): [Assignment: organization-defined time period] |
| `odp.03_13_10` | value | public | DoD ODP 03.13.10 (Rev 3 03.13.10): [Assignment: organization-defined requirements for key generation, distribution, storage, access, and destruction] |
| `odp.03_13_11` | value | public | DoD ODP 03.13.11 (Rev 3 03.13.11): [Assignment: organization-defined types of cryptography] |
| `odp.03_13_12_a` | value | public | DoD ODP 03.13.12.a (Rev 3 03.13.12): [Assignment: organization-defined exceptions where remote activation is to be allowed] |
| `odp.03_14_01_b` | value | public | DoD ODP 03.14.01.b (Rev 3 03.14.01): [Assignment: organization-defined time period] |
| `odp.03_14_02_c_01` | value | public | DoD ODP 03.14.02.c.01 (Rev 3 03.14.02): [Assignment: organization-defined frequency] |
| `odp.03_15_01_b` | value | public | DoD ODP 03.15.01.b (Rev 3 03.15.01): [Assignment: organization-defined frequency] |
| `odp.03_15_02_b` | value | public | DoD ODP 03.15.02.b (Rev 3 03.15.02): [Assignment: organization-defined frequency] |
| `odp.03_15_03_d` | value | public | DoD ODP 03.15.03.d (Rev 3 03.15.03): [Assignment: organization-defined frequency] |
| `odp.03_16_01` | value | public | DoD ODP 03.16.01 (Rev 3 03.16.01): [Assignment: organization-defined systems security engineering principles] |
| `odp.03_16_03_a` | value | public | DoD ODP 03.16.03.a (Rev 3 03.16.03): [Assignment: organization-defined security requirements] |
| `odp.03_17_01_b` | value | public | DoD ODP 03.17.01.b (Rev 3 03.17.01): [Assignment: organization-defined frequency] |
| `odp.03_17_03_b` | value | public | DoD ODP 03.17.03.b (Rev 3 03.17.03): [Assignment: organization-defined security requirements] |

<!-- odp:end -->
