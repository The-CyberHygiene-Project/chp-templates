### 3.2 System Components

{{system.name}} runs the CyberHygiene Project appliance, version {{system.appliance_version}}. It has two roles: one
**identity server** and the site's **client workstations**. Both are installed from the same signed installer image and
configured from the site's own settings on the site stick. Every host runs Rocky Linux 9 with the CUI security profile
applied at install, and nothing is configured by hand. Each component below names the record in the appliance's
project files that proves it.

**On the identity server:**

- **Kanidm identity server:** the single source of user accounts, groups and credentials for the domain {{site.domain}};
  it is installed from signed packages and serves only over TLS (evidence: idm-assistant lab/iso-requirements.md#1;
  lab/iso5/PROOF-RECORD.md).
- **step-ca certificate authority:** issues the identity server's TLS certificate. The certificate is renewed daily and
  is re-issued automatically over ACME if it has expired, for example after a long power outage (evidence:
  idm-assistant lab/iso-requirements.md#26; lab/iso5/PROOF-RECORD.md).
- **SSH certificate authority:** signs each user's SSH key with a short-lived certificate and records every certificate
  it issues; clients trust only this authority's pinned key (evidence: idm-assistant lab/iso-requirements.md#34;
  lab/iso-requirements.md#35).
- **BIND DNS:** serves the site's zone, built from the host table on the site stick (evidence: idm-assistant
  lab/iso5/PROOF-RECORD.md).

**On every host (server and clients):**

- **kanidm-unixd and authselect:** each client signs users in against Kanidm with its own read-only token, through an
  authselect profile that keeps the CUI profile's account-lockout features (evidence: idm-assistant
  lab/iso-requirements.md#8; lab/iso-requirements.md#41).
- **Google Authenticator second factor:** every Kanidm user signs in with a key or password **and** a time-based code
  for SSH, the console, sudo and the desktop. Codes are stored on each host, outside users' home folders (evidence:
  idm-assistant lab/iso-requirements.md#10; lab/iso-requirements.md#11; lab/iso-requirements.md#36).
- **USBGuard:** blocks USB storage. Only the site stick, pinned by its USB identity and hash, can be authorized
  temporarily, by the appliance's own tools (evidence: idm-assistant lab/iso-requirements.md#38;
  lab/aide/PROOF-RECORD.md).
- **fapolicyd:** application allow-listing. Only software installed from trusted, signed packages may run (evidence:
  idm-assistant lab/iso-requirements.md#1; lab/iso-requirements.md#21).
- **LUKS disk encryption with TPM unlock:** every disk is encrypted and bound to the host's TPM under Secure Boot. The
  escrowed passphrase on the site stick is the fallback (evidence: idm-assistant lab/iso-requirements.md#15;
  lab/iso5/PROOF-RECORD.md).
- **FIPS mode:** every host runs in FIPS mode, and step-ca is run with its FIPS setting (evidence: idm-assistant
  lab/iso-requirements.md#13; lab/iso-requirements.md#14).
- **AIDE file integrity:** a baseline is built at the end of first boot and checked daily. The CHP monitor alerts on
  any change, and a baseline changes only through an audited approval by the ISSO or a named delegate (evidence:
  idm-assistant lab/aide/PROOF-RECORD.md; appliance/release/RELEASE-RECORD-ISO-0.2.0.md).
- **CHP monitor:** runs the appliance's health and security checks and sends every alert to the journal and to the
  site's alert hook (evidence: idm-assistant lab/iso-requirements.md#24; lab/aide/PROOF-RECORD.md).
- **chrony time synchronization:** all hosts follow the site's time source (evidence: idm-assistant
  lab/iso-requirements.md#18; lab/iso-requirements.md#30).
- **SELinux:** enforcing on every host, including a policy for the identity client's socket (evidence: idm-assistant
  lab/iso-requirements.md#12; lab/iso-requirements.md#33).

### 3.3 The Site Stick

The **site stick** is a USB drive that holds the site's settings and, after installation, every host's recovery
secrets. It is the only removable storage the hosts accept, and only while an appliance tool is using it. It must be
kept locked up between uses, and never copied to a share or cloud folder.

### 3.4 Compliance Baseline

Every host is installed with the CUI security profile. The appliance's release record lists the release gates each
version passed, including the CUI compliance scan and its documented deviations (evidence: idm-assistant
lab/iso5/DEVIATIONS.md; appliance/release/RELEASE-RECORD-ISO-0.2.0.md).
