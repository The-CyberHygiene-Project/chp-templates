# SYSTEM SECURITY PLAN

## NIST SP 800-171 Rev 2 Compliance

Example Manufacturing LLC (doing business as Example Parts)\
**System Name:** Example Parts CUI Enclave\
**Domain:** example.test\
**Version:** 1.0 **Date:** 10/24/2026\
**Classification:** CUI

**Distribution Notice:** This document contains confidential details of Example Manufacturing LLC's security
controls. Distribution is limited to the people named in Document Control and to assessors authorized by the System
Owner.

## DOCUMENT CONTROL

**Document Status:** Draft\
**Security Classification:** CONTROLLED UNCLASSIFIED INFORMATION (CUI)\
**Distribution:** Limited to authorized personnel only

| Name / Title | Role | Signature / Date |
|:---|:---|:---|
| Alex Example, Owner | System Owner | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |
| Alex Example, Owner | ISSO | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |

**Review Schedule:** every 3 months, and upon any significant change to the system\
**Next Review Date:** 01/24/2027

### Document Revision History

| Version | Date | Author | Description |
|:---|:---|:---|:---|
| 1.0 | 10/24/2026 | Alex Example | **Initial issue.** Generated from chp-templates 1.0.0. |

Add each later revision as a new row **above** the previous one (newest first). Use MM/DD/YYYY dates and begin the
description with a bold lead sentence.

## EXECUTIVE SUMMARY

### 1.1 Purpose

This System Security Plan documents the security requirements of NIST SP 800-171 Revision 2 as they are met for
**Example Parts CUI Enclave**, which processes, stores and transmits Controlled Unclassified Information (CUI) for
Example Manufacturing LLC. It describes the system boundary, the operating environment, and how each requirement is
implemented, and it is the reference for the companion Plan of Action and Milestones (POA&M).

### 1.2 System Overview

Example Parts CUI Enclave is built on the CyberHygiene Project appliance: an identity server and enrolled client workstations
installed from a signed installer image and configured from the site's own settings. Section 3 describes the
components; Section 4 describes each requirement's implementation, and states plainly where the site, not the appliance,
is responsible.

| Measure | Definition | Value |
|:---|:---|:---|
| **SPRS score** | The DoD Assessment Methodology score (weighted 1-, 3- and 5-point deductions; Rev 2 basis). Assessed not yet assessed. **Basis:** Not yet assessed. | **0 (not yet assessed)** |
| **Strict 800-171A objectives met** | Requirements for which **every** SP 800-171A assessment objective is satisfied, or not applicable with a stated reason; unweighted and not derived from SPRS. Assessed not yet assessed. | **0/110** |

**POA&M reference:** Example POA&M v1.0 (the companion document; see Section 10).

### 1.3 Compliance Requirements

**Primary requirements:**

- NIST SP 800-171 Rev 2: Protecting CUI in Nonfederal Systems and Organizations
- FIPS 140: Cryptographic Module Validation (the appliance runs its hosts in FIPS mode)
- FAR 52.204-21: Basic Safeguarding of Covered Contractor Information Systems
- DFARS 252.204-7012: Safeguarding Covered Defense Information and Cyber Incident Reporting
- CMMC Level 2

**Supporting standards:** NIST SP 800-53 Rev 5 and NIST SP 800-171A.

**Contracts in scope:**

- Example Prime Corp purchase order (DFARS 252.204-7012)

### 1.4 Key Findings

**Strengths:**

- Every host built from the signed appliance image.

**Outstanding deficits** (each is an item in the POA&M):

- See the POA&M.

### 1.5 Authorization

This plan is approved by the System Owner and the ISSO (see Authorization).

## 2. SYSTEM IDENTIFICATION

### 2.1 System Information

| Item | Value |
|:---|:---|
| System name | Example Parts CUI Enclave |
| Domain | example.test |
| Time zone | America/Denver |
| Operational status | Operational |

### 2.2 Organization Information

| Item | Value |
|:---|:---|
| Legal name | Example Manufacturing LLC |
| Doing business as | Example Parts |
| Location | Springfield, ST |
| UEI | EXAMPLEUEI00 |
| CAGE code | EX000 |

### 2.3 Contact Information

| Role | Name | Contact |
|:---|:---|:---|
| System Owner | Alex Example, Owner | owner@example.test |
| ISSO | Alex Example, Owner | owner@example.test |
| System Administrator | Sam Sample | |

### 2.4 System Categorization

The system handles these categories of CUI:

- CUI//SP-CTI (controlled technical information)
- CUI//EXPT (export controlled)

### 2.5 System Boundary

The boundary is the identity server and the two workstations on the site network.

**Systems inside the boundary:**

- srv1.example.test (identity server)
- ws1.example.test (engineering workstation)
- ws2.example.test (office workstation)

*Not applicable: facts.has_outside_it_provider = no.*

## 3. SYSTEM DESCRIPTION

### 3.1 System Purpose and Functions

Stores and processes CUI received under defense subcontracts for machined parts.

### 3.2 System Components

Example Parts CUI Enclave runs the CyberHygiene Project appliance, version 0.2.0. It has two roles: one
**identity server** and the site's **client workstations**. Both are installed from the same signed installer image and
configured from the site's own settings on the site stick. Every host runs Rocky Linux 9 with the CUI security profile
applied at install, and nothing is configured by hand. Each component below names the record in the appliance's
project files that proves it.

**On the identity server:**

- **Kanidm identity server:** the single source of user accounts, groups and credentials for the domain example.test;
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

## 4. SECURITY CONTROL IMPLEMENTATION

Each requirement below carries its status:

- **appliance:** implemented and proven by the appliance;
- **partial:** partly implemented by the appliance, and completed by the site;
- **site:** the site's responsibility.

"Evidence" points to the appliance's own proof records.

### 4.1 Access Control (AC)

#### 3.1.1 Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#41`; idm-assistant `lab/iso-requirements.md#38`; idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `no_empty_passwords`; scan rule `sshd_disable_root_login`.

**Implementation:** Every person signs in with their own Kanidm account. Clients admit only members of the site's login group, and the server only administrators. Each client authenticates to the identity server with its own read-only token. USBGuard admits no unknown USB device. Empty passwords and direct root SSH logins are refused.

**Site responsibility:** Decide who is authorized. Add and remove accounts promptly (onboarding and revocation with the appliance's tools), and keep the lists of authorized users and devices current.

#### 3.1.2 Limit system access to the types of transactions and functions that authorized users are permitted to execute.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; idm-assistant `lab/iso-requirements.md#40`; scan rule `selinux_state`; scan rule `selinux_policytype`.

**Implementation:** Users and administrators are separate groups. Ordinary users may sign in to client workstations; only administrators have sudo. SELinux runs enforcing with the targeted policy on every host.

**Site responsibility:** Define which transactions and functions each role may perform, and place people in the matching group only.

#### 3.1.3 Control the flow of CUI in accordance with approved authorizations.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `service_firewalld_enabled`.

**Implementation:** firewalld is enabled on every host, with only the services each role needs opened.

**Site responsibility:** Define where CUI may flow (systems, people, outside parties), enforce it at the site's network boundary, and record the approved flows.

#### 3.1.4 Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance supports separation of duties: accepting a new file-integrity baseline and re-enabling an expired account each require the ISSO or a named delegate, and each approval is audited.

**Site responsibility:** Assign duties so that no single person can misuse the system without collusion. Where the business is too small to separate duties, record the compensating review.

#### 3.1.5 Employ the principle of least privilege, including for specific security functions and privileged accounts.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `sshd_disable_root_login`; scan rule `use_pam_wheel_for_su`; scan rule `sysctl_kernel_dmesg_restrict`.

**Implementation:** Root cannot sign in over SSH, su is limited to the wheel group, and administrative rights come only from membership of the administrators group. Kernel messages are readable by privileged users only.

**Site responsibility:** Grant each person only the access their job needs, and review group memberships every 3 months.

#### 3.1.6 Use non-privileged accounts or roles when accessing nonsecurity functions

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#43`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** People sign in with ordinary Kanidm accounts and use sudo for administration. The local break-glass account exists for recovery only.

**Site responsibility:** Require administrators to use their ordinary account for non-security work, and keep the break-glass key locked away.

#### 3.1.7 Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#11`; idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `audit_basic_configuration`; scan rule `audit_ospp_general`; scan rule `use_pam_wheel_for_su`.

**Implementation:** Only administrators can run privileged commands, through sudo with a second-factor code. auditd records privileged command execution on every host.

**Site responsibility:** Review the audit records of privileged commands as part of routine log review.

#### 3.1.8 Limit unsuccessful logon attempts.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#27`; scan rule `accounts_passwords_pam_faillock_deny`; scan rule `accounts_passwords_pam_faillock_interval`; scan rule `accounts_passwords_pam_faillock_unlock_time`.

**Implementation:** faillock locks an account after 3 failed attempts within 15 minutes, on every host, and keeps it locked for 0 minutes (a value of 0 means until an administrator unlocks it). The setting is pinned in the appliance's authselect profile.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.1.9 Provide privacy and security notices consistent with applicable CUI rules.

**Status:** partial. **Evidence:** scan rule `sshd_enable_warning_banner`.

**Implementation:** SSH shows a system-use notice before sign-in.

**Site responsibility:** Review the notice text against the CUI rules that apply to the site, and show an equivalent notice at every other access point.

#### 3.1.10 Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This version of the appliance does not configure a session lock.

**Site responsibility:** Configure a screen lock after 15 minutes of inactivity, with the screen's contents hidden, on every desktop and console.

#### 3.1.11 Terminate (automatically) a user session after a defined condition.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This version of the appliance does not configure automatic session termination.

**Site responsibility:** Define the conditions (such as idle time) after which a user session ends, and configure them on every host.

#### 3.1.12 Monitor and control remote access sessions.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; scan rule `disable_host_auth`; scan rule `sshd_disable_gssapi_auth`; scan rule `sshd_disable_kerb_auth`.

**Implementation:** Remote access to the appliance is SSH only, with a key or certificate plus a second-factor code. Host-based, GSSAPI and Kerberos SSH authentication are disabled. Sessions are recorded in the audit log and the journal.

**Site responsibility:** Monitor remote access sessions in the logs, and control any remote access path outside the appliance.

#### 3.1.13 Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

**Status:** appliance. **Evidence:** scan rule `enable_fips_mode`; scan rule `configure_crypto_policy`; scan rule `sshd_rekey_limit`.

**Implementation:** Every host runs in FIPS mode, and SSH uses only the FIPS system crypto policy, with session keys renegotiated at the configured limit.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.1.14 Route remote access via managed access control points.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** SSH is the only remote access service on the appliance's hosts.

**Site responsibility:** Route any remote access from outside the site through a managed access control point, such as a VPN on the site's firewall, and record it.

#### 3.1.15 Authorize remote execution of privileged commands and remote access to security-relevant information.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#11`; idm-assistant `lab/iso-requirements.md#10`.

**Implementation:** Privileged commands require sudo with a second-factor code, and only for members of the administrators group.

**Site responsibility:** Authorize the remote use of privileged commands explicitly, and record each authorization.

#### 3.1.16 Authorize wireless access prior to allowing such connections

**Status:** partial. **Evidence:** scan rule `kernel_module_bluetooth_disabled`.

**Implementation:** The Bluetooth kernel module is disabled on every host, and the appliance's hosts are cabled.

**Site responsibility:** Authorize any wireless access before allowing it.

#### 3.1.17 Protect wireless access using authentication and encryption

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance's hosts use cabled networking.

**Site responsibility:** Protect any wireless network that reaches CUI systems with authentication and encryption, for example WPA3-Enterprise.

#### 3.1.18 Control connection of mobile devices.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Mobile devices are not part of the appliance.

**Site responsibility:** Control the connection of mobile devices, and record which are allowed.

#### 3.1.19 Encrypt CUI on mobile devices and mobile computing platforms.[23]

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance encrypts its own hosts' disks (Section 3.2), but that does not cover mobile devices.

**Site responsibility:** Encrypt CUI on mobile devices and mobile computing platforms.

#### 3.1.20 Verify and control/limit connections to and use of external systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not connect to external systems for its own functions.

**Site responsibility:** Verify and control connections to and use of external systems, and list them in the boundary description.

#### 3.1.21 Limit use of portable storage devices on external systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** USBGuard blocks USB storage on the appliance's own hosts.

**Site responsibility:** Limit the use of portable storage devices on external systems.

#### 3.1.22 Control CUI posted or processed on publicly accessible systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not publish information.

**Site responsibility:** Control CUI posted or processed on publicly accessible systems: name who may post, and review content before it is posted.

### 4.2 Awareness and Training (AT)

#### 3.2.1 Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not provide training.

**Site responsibility:** Make managers, administrators and users aware of the security risks of their work and of the policies, standards and procedures that apply.

#### 3.2.2 Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not provide training.

**Site responsibility:** Train personnel to carry out their information-security duties, and keep a record of the training.

#### 3.2.3 Provide security awareness training on recognizing and reporting potential indicators of insider threat.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not provide training.

**Site responsibility:** Provide security awareness training on recognizing and reporting potential insider threats.

### 4.3 Audit and Accountability (AU)

#### 3.3.1 Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity

**Status:** partial. **Evidence:** scan rule `service_auditd_enabled`; scan rule `audit_basic_configuration`; scan rule `audit_ospp_general`; scan rule `grub2_audit_argument`; scan rule `auditd_data_retention_flush`.

**Implementation:** auditd runs on every host from boot, with the CUI profile's rules. These record failed access, permission and ownership changes, deletions, privileged commands and logins. Records are flushed to disk as they are written.

**Site responsibility:** Retain audit records for 90 days, including copies kept off the host, so they remain available for investigation.

#### 3.3.2 Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions.

**Status:** appliance. **Evidence:** scan rule `audit_immutable_login_uids`; scan rule `service_auditd_enabled`.

**Implementation:** Audit records carry each user's login ID, which cannot be changed after login, so every action traces to an individual.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.3.3 Review and update logged events.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance installs the CUI profile's audit rules.

**Site responsibility:** Review and update the logged events every 3 months.

#### 3.3.4 Alert in the event of an audit logging process failure.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** auditd is configured by the CUI profile on every host.

**Site responsibility:** Configure, and test, an alert when audit logging fails.

#### 3.3.5 Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Audit records are kept on each host, and the appliance's collector can gather them for review.

**Site responsibility:** Correlate audit review, analysis and reporting across hosts, to investigate and respond to unlawful or unauthorized activity.

#### 3.3.6 Provide audit record reduction and report generation to support on-demand analysis and reporting.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `service_auditd_enabled`.

**Implementation:** ausearch and aureport are installed with auditd on every host, for on-demand reduction and reporting.

**Site responsibility:** Use them, or a central tool, to produce the reports that analysis and investigations need.

#### 3.3.7 Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#18`; idm-assistant `lab/iso-requirements.md#30`; scan rule `chronyd_client_only`.

**Implementation:** All hosts synchronize their clocks with chrony from the site's time source, so audit timestamps agree across hosts.

**Site responsibility:** Keep the site's time source accurate and authoritative.

#### 3.3.8 Protect audit information and audit logging tools from unauthorized access, modification, and deletion.

**Status:** appliance. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; scan rule `partition_for_var_log_audit`; scan rule `mount_option_var_log_audit_nodev`; scan rule `mount_option_var_log_audit_nosuid`; scan rule `mount_option_var_log_audit_noexec`; scan rule `aide_check_audit_tools`.

**Implementation:** Audit logs live on their own partition, mounted nodev, nosuid and noexec, and readable by root only. AIDE watches the audit tools for any change.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.3.9 Limit management of audit logging functionality to a subset of privileged users.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `use_pam_wheel_for_su`.

**Implementation:** Only administrators, through sudo, can read or manage the audit logs and audit settings.

**Site responsibility:** Limit membership of the administrators group to the people who manage audit logging.

### 4.4 Configuration Management (CM)

#### 3.4.1 Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

**Status:** partial. **Evidence:** idm-assistant `appliance/release/RELEASE-RECORD-ISO-0.2.0.md`; idm-assistant `lab/aide/PROOF-RECORD.md`; idm-assistant `lab/iso5/DEVIATIONS.md`.

**Implementation:** Every host is built from the same signed installer image, with the CUI profile applied at install. The release record pins the image and package versions. Each host's AIDE baseline records its files as installed. The site stick's host table lists every machine in the boundary.

**Site responsibility:** Keep the hardware and software inventory current, including anything outside the appliance, and review it every 3 months.

#### 3.4.2 Establish and enforce security configuration settings for information technology products employed in organizational systems.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso5/DEVIATIONS.md`; idm-assistant `appliance/release/RELEASE-RECORD-ISO-0.2.0.md`; scan rule `enable_authselect`; scan rule `configure_crypto_policy`; scan rule `enable_fips_mode`.

**Implementation:** The CUI security profile is applied to every host at install and verified by a scan at each release. The documented deviations are accepted by the ISSO (evidence: the deviation table).

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.4.3 Track, review, approve or disapprove, and log changes to organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; idm-assistant `lab/iso-requirements.md#47`.

**Implementation:** AIDE checks every host's files daily and alerts on any change. A new baseline is accepted only by the ISSO or a named delegate, with a stated reason, and the acceptance is audited.

**Site responsibility:** Run a change-control process: propose, review, approve or reject, and record each change to the system.

#### 3.4.4 Analyze the security impact of changes prior to implementation.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance reports file changes after they happen (AIDE), but it does not analyse changes beforehand.

**Site responsibility:** Analyze the security impact of each change before it is made, and record the analysis with the change.

#### 3.4.5 Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; scan rule `grub2_password`; scan rule `require_singleuser_auth`; scan rule `service_debug-shell_disabled`; scan rule `disable_ctrlaltdel_reboot`; scan rule `disable_ctrlaltdel_burstaction`.

**Implementation:** Only signed packages can be installed. The boot loader is password-protected, single-user mode requires authentication, the debug shell is disabled, and Ctrl-Alt-Del cannot reboot a host.

**Site responsibility:** Define who may make changes, and restrict physical access to the hosts accordingly.

#### 3.4.6 Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `kernel_module_sctp_disabled`; scan rule `kernel_module_can_disabled`; scan rule `kernel_module_tipc_disabled`; scan rule `service_kdump_disabled`.

**Implementation:** Each role installs only the packages it needs. Unneeded kernel network modules, kdump and core dumps are disabled.

**Site responsibility:** Keep added software and services to what the business needs, and review them every 3 months.

#### 3.4.7 Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; scan rule `service_firewalld_enabled`; scan rule `service_fapolicyd_enabled`; scan rule `service_systemd-coredump_disabled`.

**Implementation:** firewalld opens only the services each role needs, and fapolicyd lets only trusted, signed software run.

**Site responsibility:** Review the open ports, protocols and services, and restrict any the business does not need.

#### 3.4.8 Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; idm-assistant `lab/iso-requirements.md#21`; scan rule `service_fapolicyd_enabled`; scan rule `package_fapolicyd_installed`; scan rule `ensure_gpgcheck_globally_activated`; scan rule `ensure_gpgcheck_never_disabled`.

**Implementation:** fapolicyd applies a permit-by-exception policy: only software installed from trusted, signed packages may run. Package signature checking is on everywhere.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.4.9 Control and monitor user-installed software.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; idm-assistant `lab/aide/PROOF-RECORD.md`; scan rule `service_fapolicyd_enabled`; scan rule `ensure_gpgcheck_local_packages`.

**Implementation:** Users cannot install software: only administrators can, from signed packages. fapolicyd blocks untrusted programs, and AIDE reports unexpected files.

**Site responsibility:** Approve any software an administrator installs, and review AIDE and fapolicyd alerts.

### 4.5 Identification and Authentication (IA)

#### 3.5.1 Identify system users, processes acting on behalf of users, and devices.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#41`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Every user has a unique Kanidm account. Every client host uses its own identity token, and every host has its own SSH host key.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.5.2 Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; idm-assistant `lab/iso-requirements.md#11`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Users authenticate with a key or password plus a time-based code before access is granted. Hosts authenticate to the identity server with their own tokens, over TLS.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.5.3 Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.[24] [25].

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; idm-assistant `lab/iso-requirements.md#11`; idm-assistant `lab/iso-requirements.md#36`; idm-assistant `lab/iso-requirements.md#43`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Every Kanidm user needs a second factor (a time-based code) for SSH, the console, sudo and the desktop. The local recovery accounts (the root console and the break-glass administrator) are exempt by design, so that the site can recover the hosts.

**Site responsibility:** Keep the local recovery credentials locked away (they are escrowed on the site stick), and record each use.

#### 3.5.4 Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; idm-assistant `lab/iso-requirements.md#9`.

**Implementation:** Network access uses SSH keys or certificates (challenge-response) together with single-use time-based codes. Neither can be replayed.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.5.5 Prevent reuse of identifiers for a defined period.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Accounts are created by name in Kanidm.

**Site responsibility:** Do not reuse an account name for a different person for at least the period the site defines, and record the rule.

#### 3.5.6 Disable identifiers after a defined period of inactivity.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This version of the appliance does not disable inactive accounts automatically.

**Site responsibility:** Disable accounts after 90 days of inactivity, for example with a scheduled review using the appliance's account tools.

#### 3.5.7 Enforce a minimum password complexity and change of characters when new passwords are created.

**Status:** partial. **Evidence:** scan rule `accounts_password_pam_minlen`; scan rule `accounts_password_pam_dcredit`; scan rule `accounts_password_pam_lcredit`; scan rule `accounts_password_pam_ucredit`; scan rule `accounts_password_pam_ocredit`.

**Implementation:** Local passwords must meet the CUI profile's length and character-class rules.

**Site responsibility:** Set the identity server's password policy to a minimum length of 12, and confirm that it applies to every account.

#### 3.5.8 Prohibit password reuse for a specified number of generations.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This version of the appliance does not enforce password history.

**Site responsibility:** Prohibit reuse of the last 5 passwords, and record how it is enforced.

#### 3.5.9 Allow temporary password use for system logons with an immediate change to a permanent password.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#25`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** New users are onboarded with a one-time reset token, and they set their own credentials on first use.

**Site responsibility:** Issue tokens only to the named user, and confirm that a temporary credential is changed at first sign-in.

#### 3.5.10 Store and transmit only cryptographically-protected passwords.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#13`; idm-assistant `lab/iso-requirements.md#14`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Passwords are stored only as hashes and travel only over TLS or SSH. The hosts run in FIPS mode, but the identity server's own password crypto runs outside the FIPS module; this plan records that position.

**Site responsibility:** Accept, or remediate, the identity server's crypto position, and record the decision in the POA&M.

#### 3.5.11 Obscure feedback of authentication information

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#36`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Sign-in prompts on every host hide the characters typed for passwords and codes.

**Site responsibility:** None beyond operating the appliance as documented.

### 4.6 Incident Response (IR)

#### 3.6.1 Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance raises alerts through the CHP monitor and the site's alert hook, and its diagnostic tools help analyse identity problems.

**Site responsibility:** Establish an incident-handling capability: preparation, detection and analysis, containment, recovery and user response.

#### 3.6.2 Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Alerts are written to each host's journal and sent to the site's alert hook.

**Site responsibility:** Track and document incidents, and report them to the designated officials and authorities within 72 hours where a contract requires it.

#### 3.6.3 Test the organizational incident response capability.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not test incident response.

**Site responsibility:** Test the incident response capability, for example with a yearly tabletop exercise, and record the results.

### 4.7 Maintenance (MA)

#### 3.7.1 Perform maintenance on organizational systems.[26].

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Updates are delivered as signed package repositories that install without a reinstall.

**Site responsibility:** Perform maintenance on the system, including applying updates on the site's patch cadence of monthly.

#### 3.7.2 Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; scan rule `selinux_state`; scan rule `selinux_policytype`; scan rule `service_fapolicyd_enabled`.

**Implementation:** Only signed, trusted tools can run on the hosts (fapolicyd), and SELinux confines services.

**Site responsibility:** Control the tools, techniques and people used for maintenance, and keep a record of maintenance performed.

#### 3.7.3 Ensure equipment removed for off-site maintenance is sanitized of any CUI.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Disks are encrypted (LUKS), which protects data on equipment that leaves the site.

**Site responsibility:** Sanitize equipment of CUI before it is removed for off-site maintenance.

#### 3.7.4 Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** USBGuard blocks USB storage on the hosts, except the site stick, which only the appliance's own tools may use.

**Site responsibility:** Check media containing diagnostic and test programs for malicious code before they are used.

#### 3.7.5 Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#10`; idm-assistant `lab/iso-requirements.md#11`.

**Implementation:** Remote maintenance over SSH requires a key or certificate plus a second-factor code.

**Site responsibility:** Terminate remote maintenance sessions when maintenance is complete, and record each session.

#### 3.7.6 Supervise the maintenance activities of maintenance personnel without required access authorization.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not control physical maintenance.

**Site responsibility:** Supervise the maintenance activities of personnel who do not have the required access authorization.

### 4.8 Media Protection (MP)

#### 3.8.1 Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#15`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Every host's disk is encrypted (LUKS2), with a TPM unlock bound to Secure Boot.

**Site responsibility:** Protect paper and removable media containing CUI: store them securely, and limit who can reach them.

#### 3.8.2 Limit access to CUI on system media to authorized users

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#38`; idm-assistant `lab/iso-requirements.md#15`; scan rule `service_usbguard_enabled`.

**Implementation:** Data on the hosts' disks is reachable only by signed-in, authorized users. USBGuard prevents copying CUI to USB storage.

**Site responsibility:** Limit access to CUI on paper and on removable media to authorized users.

#### 3.8.3 Sanitize or destroy system media containing CUI before disposal or release for reuse.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** Disks are encrypted, so destroying the escrowed keys renders a disk unreadable. Sanitization is still the site's job.

**Site responsibility:** Sanitize or destroy media containing CUI before disposal or reuse, and keep a record.

#### 3.8.4 Mark media with necessary CUI markings and distribution limitations.[27]

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not mark media.

**Site responsibility:** Mark media with the required CUI markings and distribution limitations.

#### 3.8.5 Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not move media.

**Site responsibility:** Control access to media containing CUI, and maintain accountability for it during transport outside controlled areas.

#### 3.8.6 Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#15`; idm-assistant `lab/iso-requirements.md#38`.

**Implementation:** Hosts' disks are encrypted, so a host moved or shipped keeps its data protected. The site stick is NOT encrypted, and it holds every host's recovery secrets.

**Site responsibility:** Transport the site stick, and any other media with CUI, under physical safeguards (sealed and accompanied), or encrypt it.

#### 3.8.7 Control the use of removable media on system components.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#38`; idm-assistant `lab/aide/PROOF-RECORD.md`; scan rule `service_usbguard_enabled`; scan rule `package_usbguard_installed`; scan rule `usbguard_allow_hid_and_hub`; scan rule `configure_usbguard_auditbackend`.

**Implementation:** USBGuard blocks USB storage on every host. Only the site stick, pinned by its USB identity and hash, can be authorized, temporarily, by the appliance's own tools. Every USBGuard decision is audited.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.8.8 Prohibit the use of portable storage devices when such devices have no identifiable owner.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#38`; scan rule `service_usbguard_enabled`.

**Implementation:** USBGuard blocks every portable storage device except the site's own pinned stick, so a device with no identifiable owner cannot be used.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.8.9 Protect the confidentiality of backup CUI at storage locations.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not hold the site's backups.

**Site responsibility:** Protect the confidentiality of backup CUI at its storage locations, for example by encrypting backups.

### 4.9 Personnel Security (PS)

#### 3.9.1 Screen individuals prior to authorizing access to organizational systems containing CUI.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not screen people.

**Site responsibility:** Screen individuals before authorizing access to systems containing CUI.

#### 3.9.2 Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#39`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** Revoking a person through the appliance expires their account, and clears the cached identity on every client so that access ends everywhere.

**Site responsibility:** Revoke access promptly when a person leaves or changes role, and recover their equipment and credentials.

### 4.10 Physical Protection (PE)

#### 3.10.1 Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not control physical access.

**Site responsibility:** Limit physical access to the systems, equipment and operating environments to authorized individuals.

#### 3.10.2 Protect and monitor the physical facility and support infrastructure for organizational systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not control the facility.

**Site responsibility:** Protect and monitor the physical facility and the support infrastructure for the systems.

#### 3.10.3 Escort visitors and monitor visitor activity.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not control visitors.

**Site responsibility:** Escort visitors, and monitor visitor activity.

#### 3.10.4 Maintain audit logs of physical access.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance keeps no record of physical access to its hosts.

**Site responsibility:** Maintain audit logs of physical access, for example a sign-in log for the room or rack, and review them.

#### 3.10.5 Control and manage physical access devices.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not manage keys or locks.

**Site responsibility:** Control and manage physical access devices such as keys, combinations and badges.

#### 3.10.6 Enforce safeguarding measures for CUI at alternate work sites.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not cover alternate work sites.

**Site responsibility:** Enforce safeguarding measures for CUI at alternate work sites, such as home offices.

### 4.11 Risk Assessment (RA)

#### 3.11.1 Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance's proof records list what the appliance itself was tested for.

**Site responsibility:** Assess the risk to operations, assets and individuals every 3 months, and record the assessment.

#### 3.11.2 Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/DEVIATIONS.md`; scan rule `package_openscap-scanner_installed`; scan rule `package_scap-security-guide_installed`.

**Implementation:** OpenSCAP and the SCAP Security Guide are installed on every host, for compliance scanning against the CUI profile.

**Site responsibility:** Scan for vulnerabilities periodically and when new vulnerabilities are announced, using a vulnerability scanner as well as the compliance scan.

#### 3.11.3 Remediate vulnerabilities in accordance with risk assessments.

**Status:** partial. **Evidence:** scan rule `package_dnf-automatic_installed`; scan rule `timer_dnf-automatic_enabled`; scan rule `dnf-automatic_apply_updates`.

**Implementation:** Automatic package updates are enabled on every host, from the site's signed update repository.

**Site responsibility:** Remediate vulnerabilities according to the risk assessment: apply critical patches within 72 hours of detection, and others on the site's cadence (monthly).

### 4.12 Security Assessment (CA)

#### 3.12.1 Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance provides the compliance scan and its own proof records as inputs.

**Site responsibility:** Assess the security controls periodically to determine whether they are effective, and record the results.

#### 3.12.2 Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** A POA&M template, pre-seeded with the appliance's known gaps, comes with this plan.

**Site responsibility:** Develop and implement the POA&M to correct deficiencies and reduce or eliminate vulnerabilities.

#### 3.12.3 Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.

**Status:** partial. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; idm-assistant `lab/iso-requirements.md#24`.

**Implementation:** The CHP monitor runs its security checks continuously, and AIDE checks every host's files daily. Every alert goes to the journal and to the site's alert hook.

**Site responsibility:** Watch the alerts, and act on each one.

#### 3.12.4 Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.[28]

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This plan is generated from the project's templates and describes the appliance as released.

**Site responsibility:** Keep this plan current: update it when the system changes, and review it every 3 months.

### 4.13 System and Communications Protection (SC)

#### 3.13.1 Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `service_firewalld_enabled`.

**Implementation:** firewalld runs on every host, and allows only the services each role needs.

**Site responsibility:** Monitor, control and protect communications at the site's external boundary (the site firewall) and at key internal boundaries.

#### 3.13.2 Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

**Status:** partial. **Evidence:** idm-assistant `appliance/release/RELEASE-RECORD-ISO-0.2.0.md`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** The appliance is built on a few principles: signed packages only, least functionality, FIPS mode, separate server and client roles, and every host configured from the same verified image.

**Site responsibility:** Apply sound security architecture to everything outside the appliance, and record the design choices.

#### 3.13.3 Separate user functionality from system management functionality.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#43`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** System management is separate from user functions. Administration needs sudo with a second factor, and the identity server's administrators are separate accounts from users.

**Site responsibility:** Keep management accounts and interfaces separate from everyday user accounts.

#### 3.13.4 Prevent unauthorized and unintended information transfer via shared system resources.

**Status:** partial. **Evidence:** scan rule `grub2_init_on_alloc_argument`; scan rule `grub2_page_alloc_shuffle_argument`; scan rule `service_systemd-coredump_disabled`; scan rule `sysctl_kernel_core_pattern_empty_string`.

**Implementation:** Memory is zeroed when allocated, page allocation is randomized, and core dumps are disabled, which limits information left behind in shared resources.

**Site responsibility:** Avoid shared resources (shared accounts, folders or devices) that could pass CUI between users.

#### 3.13.5 Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance has no publicly accessible components.

**Site responsibility:** Place any publicly accessible system on a subnetwork separated from internal networks.

#### 3.13.6 Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

**Status:** partial. **Evidence:** idm-assistant `lab/iso5/PROOF-RECORD.md`; scan rule `service_firewalld_enabled`.

**Implementation:** Inbound connections to every host are denied by default, except for the services each role needs.

**Site responsibility:** Deny network traffic by default at the site boundary, including outbound, and allow it by exception.

#### 3.13.7 Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling).

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not provide VPN access.

**Site responsibility:** Prevent remote devices from using split tunneling while connected to the system's network.

#### 3.13.8 Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#13`; idm-assistant `lab/iso-requirements.md#31`; scan rule `configure_crypto_policy`; scan rule `enable_fips_mode`; scan rule `ssh_client_rekey_limit`.

**Implementation:** All communication with the identity server is TLS, verified against the site's pinned root certificate. Administration is SSH. Both use the FIPS system crypto policy.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.13.9 Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** This version of the appliance does not end idle network sessions.

**Site responsibility:** End network connections at the end of a session or after a defined period of inactivity.

#### 3.13.10 Establish and manage cryptographic keys for cryptography employed in organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#26`; idm-assistant `lab/iso-requirements.md#31`; idm-assistant `lab/iso-requirements.md#34`; idm-assistant `lab/iso-requirements.md#15`.

**Implementation:** The appliance runs its own certificate authority (TLS certificates, renewed daily) and an SSH certificate authority. Disk keys are bound to each host's TPM. The recovery keys and passphrases are escrowed on the site stick.

**Site responsibility:** Manage the site stick as a key store: limit who holds it, keep it locked away, and record each use.

#### 3.13.11 Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#13`; idm-assistant `lab/iso-requirements.md#14`; scan rule `enable_fips_mode`; scan rule `enable_dracut_fips_module`; scan rule `configure_crypto_policy`; scan rule `aide_use_fips_hashes`.

**Implementation:** Every host runs in FIPS mode, with FIPS-approved hashing for file integrity, and step-ca runs with its FIPS setting. The identity server's own crypto runs outside the FIPS module; this plan records that position.

**Site responsibility:** Accept, or remediate, the identity server's crypto position, and record the decision in the POA&M.

#### 3.13.12 Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device.[29].

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance's servers have no cameras or microphones.

**Site responsibility:** Prohibit remote activation of collaborative computing devices (cameras, microphones) on workstations, and show users when they are in use.

#### 3.13.13 Control and monitor the use of mobile code.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; scan rule `service_fapolicyd_enabled`.

**Implementation:** fapolicyd allows only trusted, signed programs to run on the hosts.

**Site responsibility:** Control and monitor mobile code in browsers and documents (scripts, macros) on workstations.

#### 3.13.14 Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance provides no voice service.

**Site responsibility:** Control and monitor the use of Voice over IP.

#### 3.13.15 Protect the authenticity of communications sessions.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#31`; idm-assistant `lab/iso-requirements.md#35`; idm-assistant `lab/iso-requirements.md#9`.

**Implementation:** Clients trust only the site's pinned certificate authority for TLS, and only the appliance's SSH certificate authority for user certificates, so a session cannot be impersonated.

**Site responsibility:** None beyond operating the appliance as documented.

#### 3.13.16 Protect the confidentiality of CUI at rest.

**Status:** appliance. **Evidence:** idm-assistant `lab/iso-requirements.md#15`; idm-assistant `lab/iso5/PROOF-RECORD.md`.

**Implementation:** CUI at rest on every host is protected by full-disk encryption (LUKS2), unlocked by the host's TPM under Secure Boot.

**Site responsibility:** Protect CUI stored outside the hosts, such as backups and removable media.

### 4.14 System and Information Integrity (SI)

#### 3.14.1 Identify, report, and correct system flaws in a timely manner.

**Status:** partial. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; scan rule `dnf-automatic_apply_updates`; scan rule `timer_dnf-automatic_enabled`.

**Implementation:** Hosts apply updates automatically from the site's signed update repository, and AIDE reports any change to system files.

**Site responsibility:** Identify, report and correct system flaws promptly: track advisories, and apply critical fixes within 72 hours.

#### 3.14.2 Provide protection from malicious code at designated locations within organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#1`; idm-assistant `lab/iso-requirements.md#38`; scan rule `service_fapolicyd_enabled`; scan rule `selinux_state`.

**Implementation:** fapolicyd lets only trusted, signed programs run, USBGuard blocks USB storage, and SELinux confines services. The appliance has no antivirus scanner.

**Site responsibility:** Decide whether a malware scanner is also needed on workstations, and protect email and web access.

#### 3.14.3 Monitor system security alerts and advisories and take action in response.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** The appliance does not track security advisories.

**Site responsibility:** Monitor security alerts and advisories, and act on them.

#### 3.14.4 Update malicious code protection mechanisms when new releases are available.

**Status:** partial. **Evidence:** idm-assistant `lab/iso-requirements.md#46`; idm-assistant `lab/iso-requirements.md#1`.

**Implementation:** fapolicyd's list of trusted programs is updated from the package database as signed updates are installed.

**Site responsibility:** Update any additional malware protection the site uses whenever new releases are available.

#### 3.14.5 Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed.

**Status:** site. **Evidence:** none (the site's responsibility).

**Implementation:** AIDE checks every host's files daily for unexpected changes, but it is not a malware scanner.

**Site responsibility:** Perform periodic scans of the system, and real-time scans of files from external sources, with a malware scanner where one is used.

#### 3.14.6 Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

**Status:** partial. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; idm-assistant `lab/iso-requirements.md#24`.

**Implementation:** The CHP monitor and AIDE watch every host, and auditd records security events. The appliance has no network intrusion detection.

**Site responsibility:** Monitor network traffic, inbound and outbound, to detect attacks and indicators of potential attacks.

#### 3.14.7 Identify unauthorized use of organizational systems.

**Status:** partial. **Evidence:** idm-assistant `lab/aide/PROOF-RECORD.md`; scan rule `audit_basic_configuration`; scan rule `accounts_passwords_pam_faillock_deny`.

**Implementation:** Audit records, account lockouts and monitor alerts show unusual sign-in activity and unexpected changes.

**Site responsibility:** Review them regularly to identify unauthorized use of the system.

## 5. CONTINGENCY PLANNING (CP)

### System Backup

Backups are taken every day, and a restore is tested every
quarter. The appliance's recovery secrets (disk passphrases, the root console and boot-loader
passwords, the identity administrators' recovery passwords and the certificate authority's key) are held on the site
stick, which is stored as described in Appendix C. The site stick is not a backup of data.

### System Recovery

A failed host is reinstalled from the signed installer image and the site stick, then restored from backup. A host's
encrypted disk unlocks through its TPM; if the TPM binding is lost, the escrowed passphrase on the site stick unlocks it.

## 6. SECURITY POLICIES AND PROCEDURES

The policies and procedures that this plan relies on are maintained as separate documents:

- Access Control Policy v1.0
- Identification and Authentication (Password) Policy v1.0
- Incident Response Plan v1.0

## 10. PLAN OF ACTION AND MILESTONES (POA&M)

Every requirement that is not fully met is tracked in the POA&M (Example POA&M v1.0), with its weakness, milestones,
owner and scheduled completion date. The POA&M is reviewed every 3 months.

## 11. IMPLEMENTATION METRICS

### Control Family Status

| Family | Total | Met | Not Met | Unverified |
|:---|---:|---:|---:|---:|
| AC — Access Control | 22 | 0 | 0 | 0 |
| AT — Awareness and Training | 3 | 0 | 0 | 0 |
| AU — Audit and Accountability | 9 | 0 | 0 | 0 |
| CM — Configuration Management | 9 | 0 | 0 | 0 |
| IA — Identification and Authentication | 11 | 0 | 0 | 0 |
| IR — Incident Response | 3 | 0 | 0 | 0 |
| MA — Maintenance | 6 | 0 | 0 | 0 |
| MP — Media Protection | 9 | 0 | 0 | 0 |
| PS — Personnel Security | 2 | 0 | 0 | 0 |
| PE — Physical Protection | 6 | 0 | 0 | 0 |
| RA — Risk Assessment | 3 | 0 | 0 | 0 |
| CA — Security Assessment | 4 | 0 | 0 | 0 |
| SC — System and Communications Protection | 16 | 0 | 0 | 0 |
| SI — System and Information Integrity | 7 | 0 | 0 | 0 |
| **TOTAL** | **110** | **0** | **0** | **0** |

## 12. CONCLUSION

The system is operational and the open items are tracked in the POA&M.

## AUTHORIZATION

By signing, the System Owner and the ISSO confirm that this plan describes the system as it is operated, and accept the
risk of the open items in the POA&M.

| Name / Title | Role | Signature / Date |
|:---|:---|:---|
| Alex Example, Owner | System Owner | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |
| Alex Example, Owner | ISSO | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |

## APPENDICES

### Appendix A: Acronyms

| Acronym | Meaning |
|:---|:---|
| CUI | Controlled Unclassified Information |
| FIPS | Federal Information Processing Standards |
| ISSO | Information System Security Officer |
| MFA | Multi-Factor Authentication |
| POA&M | Plan of Action and Milestones |
| SPRS | Supplier Performance Risk System |
| SSP | System Security Plan |
| TPM | Trusted Platform Module |

### Appendix B: References

- NIST SP 800-171 Rev 2, Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations
- NIST SP 800-171A, Assessing Security Requirements for Controlled Unclassified Information
- DoD Assessment Methodology for NIST SP 800-171
- The CyberHygiene Project appliance release record for the installed version (0.2.0)

### Appendix C: Supporting Documentation

- Site stick: locked cabinet, office 2

### Appendix D: Document Maintenance

This plan is generated from chp-templates 1.0.0 and then maintained by the System Owner. Change it
when the system changes; record each change in the Document Revision History; review it every
3 months.

### Appendix E: Defined Parameters

| Parameter | Value |
|:---|:---|
| Failed logon attempts before lockout | 3 |
| Lockout duration (minutes; 0 = until an administrator unlocks) | 0 |
| Minimum password length | 12 |
| Password history | 5 |
| Disable inactive accounts after (days) | 90 |
| Screen lock after (minutes) | 15 |
| Audit log retention (days) | 90 |
| Patch cadence | monthly |
| Critical patches within (hours) | 72 |
| Incident reported externally within (hours) | 72 |

*Add further lettered appendices below; nothing reads their order.*
