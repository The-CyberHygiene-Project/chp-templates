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
| `templates.version` | value | public | the chp-templates release the document was generated from |
