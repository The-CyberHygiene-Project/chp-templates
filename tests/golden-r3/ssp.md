# SYSTEM SECURITY PLAN

## NIST SP 800-171 Rev 3 Compliance

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

This System Security Plan documents the security requirements of NIST SP 800-171 Revision 3 as they are met for
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
| **SPRS score** | The DoD Assessment Methodology score, on the basis the site's contracts require. Assessed not yet assessed. **Basis:** Not yet assessed. | **0 (not yet assessed)** |
| **Strict 800-171A objectives met** | Requirements for which **every** SP 800-171A Rev 3 assessment objective is satisfied, or not applicable with a stated reason; unweighted and not derived from SPRS. Assessed not yet assessed. | **0/97** |

**POA&M reference:** Example POA&M v1.0 (the companion document; see Section 10).

### 1.3 Compliance Requirements

**Primary requirements:**

- NIST SP 800-171 Rev 3: Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations
- DoD Organization-Defined Parameters for NIST SP 800-171 Revision 3 (memo signed April 10, 2025)
- FIPS 140: Cryptographic Module Validation (the appliance runs its hosts in FIPS mode)
- FAR 52.204-21: Basic Safeguarding of Covered Contractor Information Systems
- DFARS 252.204-7012: Safeguarding Covered Defense Information and Cyber Incident Reporting
- CMMC Level 2

At the time of this template, CMMC Level 2 assessments use Rev 2. Check which revision each contract requires; this plan
prepares the system for Rev 3.

**Supporting standards:** NIST SP 800-53 Rev 5 and NIST SP 800-171A Rev 3.

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

- srv1 (identity server, Rocky Linux 9)
- ws1 (engineering workstation, Rocky Linux 9)
- ws2 (office workstation, Rocky Linux 9)

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
- **site:** the site's responsibility;
- **pending:** the library's Rev 3 text is not yet written, because the control is not yet proven on the Rev 3
  reference implementation; until then the site describes its own implementation.

"Evidence" points to the appliance's own proof records.

Each requirement lists its organization-defined parameters. The DoD values are the defaults, marked *(default, not yet
confirmed)* until the site confirms or changes them in profile.ini's [odp] section.
Each requirement also names its Rev 2 basis.

### 4.1 Access Control (AC)

#### 03.01.01 Account Management

> a\. Define the types of system accounts allowed and prohibited.\
> b\. Create, enable, modify, disable, and remove system accounts in accordance with policy, procedures, prerequisites, and criteria.\
> c\. Specify:\
> 1\. Authorized users of the system,\
> 2\. Group and role membership, and\
> 3\. Access authorizations (i.e., privileges) for each account.\
> d\. Authorize access to the system based on:\
> 1\. A valid access authorization and\
> 2\. Intended system usage.\
> e\. Monitor the use of system accounts.\
> f\. Disable system accounts when:\
> 1\. The accounts have expired,\
> 2\. The accounts have been inactive for [Assignment: organization-defined time period],\
> 3\. The accounts are no longer associated with a user or individual,\
> 4\. The accounts are in violation of organizational policy, or\
> 5\. Significant risks associated with individuals are discovered.\
> g\. Notify account managers and designated personnel or roles within:\
> 1\. [Assignment: organization-defined time period] when accounts are no longer required.\
> 2\. [Assignment: organization-defined time period] when users are terminated or transferred.\
> 3\. [Assignment: organization-defined time period] when system usage or the need-to-know changes for an individual.\
> h\. Require that users log out of the system after [Assignment: organization-defined time period] of expected inactivity or when [Assignment: organization-defined circumstances].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.1; it also covers withdrawn 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.01.f.02` [Assignment: organization-defined time period]: at most 90 days
- `03.01.01.g.01` [Assignment: organization-defined time period]: 24 hours *(default, not yet confirmed)*
- `03.01.01.g.02` [Assignment: organization-defined time period]: 24 hours *(default, not yet confirmed)*
- `03.01.01.g.03` [Assignment: organization-defined time period]: 24 hours *(default, not yet confirmed)*
- `03.01.01.h.01` [Assignment: organization-defined time period]: at most 24 hours *(default, not yet confirmed)*
- `03.01.01.h.02` [Assignment: organization-defined circumstances]: the work period ends, for privileged users at a minimum *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.02 Access Enforcement

> Enforce approved authorizations for logical access to CUI and system resources in accordance with applicable access control policies.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.2; it also covers withdrawn 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.03 Information Flow Enforcement

> Enforce approved authorizations for controlling the flow of CUI within the system and between connected systems.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.3; it also covers withdrawn 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.04 Separation of Duties

> a\. Identify the duties of individuals requiring separation.\
> b\. Define system access authorizations to support separation of duties.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.4; it also covers withdrawn 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.05 Least Privilege

> a\. Allow only authorized system access for users (or processes acting on behalf of users) that is necessary to accomplish assigned organizational tasks.\
> b\. Authorize access to [Assignment: organization-defined security functions] and [Assignment: organization-defined security-relevant information].\
> c\. Review the privileges assigned to roles or classes of users [Assignment: organization-defined frequency] to validate the need for such privileges.\
> d\. Reassign or remove privileges, as necessary.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.5; it also covers withdrawn 3.4.9, 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.05.b.01` [Assignment: organization-defined security functions]: at a minimum and if applicable: establishing system accounts and assigning privileges, configuring access authorizations, configuring settings for events to be audited, establishing vulnerability scanning parameters, establishing intrusion detection parameters, and managing audit information *(default, not yet confirmed)*
- `03.01.05.b.02` [Assignment: organization-defined security-relevant information]: at a minimum and if applicable: threat and vulnerability information, filtering rules for routers or firewalls, configuration parameters for security services, cryptographic key management information, security architecture, access control lists, and audit information *(default, not yet confirmed)*
- `03.01.05.c` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.06 Least Privilege – Privileged Accounts

> a\. Restrict privileged accounts on the system to [Assignment: organization-defined personnel or roles].\
> b\. Require that users (or roles) with privileged accounts use non-privileged accounts when accessing non-security functions or non-security information.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.6; it also covers withdrawn 3.4.9, 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.06.a` [Assignment: organization-defined personnel or roles]: only defined and authorized personnel or administrative roles *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.07 Least Privilege – Privileged Functions

> a\. Prevent non-privileged users from executing privileged functions.\
> b\. Log the execution of privileged functions.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.7; it also covers withdrawn 3.4.9, 3.13.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.08 Unsuccessful Logon Attempts

> a\. Enforce a limit of [Assignment: organization-defined number] consecutive invalid logon attempts by a user during a [Assignment: organization-defined time period].\
> b\. Automatically [Selection (one or more): lock the account or node for an [Assignment: organization-defined time period]; lock the account or node until released by an administrator; delay next logon prompt; notify system administrator; take other action] when the maximum number of unsuccessful attempts is exceeded.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.8. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.1.8.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.08.a.01` [Assignment: organization-defined number]: at most five (5) *(default, not yet confirmed)*
- `03.01.08.a.02` [Assignment: organization-defined time period]: period of five (5) minutes *(default, not yet confirmed)*
- `03.01.08.b` [Assignment: organization-defined time period]: [Selection (one or more): lock the account or node for an at least 15-minute time period; lock the account or node until released by an administrator and notify a system administrator] *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.09 System Use Notification

> Display a system use notification message with privacy and security notices consistent with applicable CUI rules before granting access to the system.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.9. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.1.9.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.10 Device Lock

> a\. Prevent access to the system by [Selection (one or more): initiating a device lock after [Assignment: organization-defined time period] of inactivity; requiring the user to initiate a device lock before leaving the system unattended].\
> b\. Retain the device lock until the user reestablishes access using established identification and authentication procedures.\
> c\. Conceal, via the device lock, information previously visible on the display with a publicly viewable image.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.10. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.1.10.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.10.a` [Assignment: organization-defined time period]: initiating a device lock after “at most 15 minutes” of inactivity and requiring the user to initiate a device lock before leaving the system unattended *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.11 Session Termination

> Terminate a user session automatically after [Assignment: organization-defined conditions or trigger events requiring session disconnect].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.11. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.1.11.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.11` [Assignment: organization-defined conditions or trigger events requiring session disconnect]: a specified duration (maximum of 24 hours) of inactivity, misbehavior (end the session due to an attempted policy violation), and maintenance (terminate sessions to prevent issues with an upgrade or service outage) *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.12 Remote Access

> a\. Establish usage restrictions, configuration requirements, and connection requirements for each type of allowable remote system access.\
> b\. Authorize each type of remote system access prior to establishing such connections.\
> c\. Route remote access to the system through authorized and managed access control points.\
> d\. Authorize the remote execution of privileged commands and remote access to security-relevant information.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.12; it also covers withdrawn 3.1.13, 3.1.14, 3.1.15, 3.13.7. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.16 Wireless Access

> a\. Establish usage restrictions, configuration requirements, and connection requirements for each type of wireless access to the system.\
> b\. Authorize each type of wireless access to the system prior to establishing such connections.\
> c\. Disable, when not intended for use, wireless networking capabilities prior to issuance and deployment.\
> d\. Protect wireless access to the system using authentication and encryption.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.16; it also covers withdrawn 3.1.17. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.18 Access Control for Mobile Devices

> a\. Establish usage restrictions, configuration requirements, and connection requirements for mobile devices.\
> b\. Authorize the connection of mobile devices to the system.\
> c\. Implement full-device or container-based encryption to protect the confidentiality of CUI on mobile devices.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.18; it also covers withdrawn 3.1.19. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.20 Use of External Systems

> a\. Prohibit the use of external systems unless the systems are specifically authorized.\
> b\. Establish the following security requirements to be satisfied on external systems prior to allowing use of or access to those systems by authorized individuals: [Assignment: organization-defined security requirements].\
> c\. Permit authorized individuals to use external systems to access the organizational system or to process, store, or transmit CUI only after:\
> 1\. Verifying that the security requirements on the external systems as specified in the organization’s system security plans have been satisfied and\
> 2\. Retaining approved system connection or processing agreements with the organizational entities hosting the external systems.\
> d\. Restrict the use of organization-controlled portable storage devices by authorized individuals on external systems.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.20; it also covers withdrawn 3.1.21. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.01.20.b` [Assignment: organization-defined security requirements]: {{odp.03_01_20_b}} *DoD gives guidance, not a value: Organizations establish specific terms and conditions for the use of external systems in accordance with organizational security policies and procedures. At a minimum, terms and conditions address the specific types of applications that can be accessed on organizational systems from external systems and the highest security category of information that can be processed, stored, or transmitted on external systems. If the terms and conditions with the owners of the external systems cannot be established, organizations may impose restrictions on organizational personnel using those external systems. If applicable, use NIST SP 800-47 as a guide for establishing information exchanges between organizations.*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.01.22 Publicly Accessible Content

> a\. Train authorized individuals to ensure that publicly accessible information does not contain CUI.\
> b\. Review the content on publicly accessible systems for CUI and remove such information, if discovered.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.1.22. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.1.22.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.2 Awareness and Training (AT)

#### 03.02.01 Literacy Training and Awareness

> a\. Provide security literacy training to system users:\
> 1\. As part of initial training for new users and [Assignment: organization-defined frequency] thereafter,\
> 2\. When required by system changes or following [Assignment: organization-defined events], and\
> 3\. On recognizing and reporting indicators of insider threat, social engineering, and social mining.\
> b\. Update security literacy training content [Assignment: organization-defined frequency] and following [Assignment: organization-defined events].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.2.1; it also covers withdrawn 3.2.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.02.01.a.01` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.02.01.a.02` [Assignment: organization-defined events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*
- `03.02.01.b.01` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.02.01.b.02` [Assignment: organization-defined events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.02.02 Role-Based Training

> a\. Provide role-based security training to organizational personnel:\
> 1\. Before authorizing access to the system or CUI, before performing assigned duties, and [Assignment: organization-defined frequency] thereafter.\
> 2\. When required by system changes or following [Assignment: organization-defined events].\
> b\. Update role-based training content [Assignment: organization-defined frequency] and following [Assignment: organization-defined events].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.2.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.2.2.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.02.02.a.01` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.02.02.a.02` [Assignment: organization-defined events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*
- `03.02.02.b.01` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.02.02.b.02` [Assignment: organization-defined events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.3 Audit and Accountability (AU)

#### 03.03.01 Event Logging

> a\. Specify the following event types selected for logging within the system: [Assignment: organization-defined event types].\
> b\. Review and update the event types selected for logging [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.03.01.a` [Assignment: organization-defined event types]: at a minimum and where applicable: 1) Authentication events: a) Logons (Success/Failure) b) Logoffs (Success) 2) Security Relevant File and Objects events: a) Create (Success/Failure) b) Access (Success/Failure) c) Delete (Success/Failure) d) Modify (Success/Failure) e) Permission Modification (Success/Failure) f) Ownership Modification (Success/Failure) 3) Export/Writes/downloads to devices/digital media (e.g., CD/DVD, USB, SD) (Success/Failure) 4) Import/Uploads from devices/digital media (e.g., CD/DVD, USB, SD) (Success/Failure) 5) User and Group Management events: a) User add, delete, modify, disable, lock (Success/Failure) b) Group/Role add, delete, modify (Success/Failure) 6) Use of Privileged/Special Rights events: a) Security or audit policy changes (Success/Failure) b) Configuration changes (Success/Failure) 7) Admin or root-level access (Success/Failure) 8) Privilege/Role escalation (Success/Failure) 9) Audit and security relevant log data accesses (Success/Failure) 10) System reboot, restart, and shutdown (Success/Failure) 11) Print to a device (Success/Failure) 12) Print to a file (e.g., pdf format) (Success/Failure) 13) Application (e.g., Adobe, Firefox, MS Office Suite) initialization (Success/Failure) For additional guidance, see: OMB21-31 ML 1 *(default, not yet confirmed)*
- `03.03.01.b` [Assignment: organization-defined frequency]: at least every 12 months and after any significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.02 Audit Record Content

> a\. Include the following content in audit records:\
> 1\. What type of event occurred\
> 2\. When the event occurred\
> 3\. Where the event occurred\
> 4\. Source of the event\
> 5\. Outcome of the event\
> 6\. Identity of the individuals, subjects, objects, or entities associated with the event\
> b\. Provide additional information for audit records as needed.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.2.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.03 Audit Record Generation

> a\. Generate audit records for the selected event types and audit record content specified in 03.03.01 and 03.03.02.\
> b\. Retain audit records for a time period consistent with the records retention policy.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.3. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.04 Response to Audit Logging Process Failures

> a\. Alert organizational personnel or roles within [Assignment: organization-defined time period] in the event of an audit logging process failure.\
> b\. Take the following additional actions: [Assignment: organization-defined additional actions].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.4.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.03.04.a` [Assignment: organization-defined time period]: near real time or as soon as practicable upon discovery *(default, not yet confirmed)*
- `03.03.04.b` [Assignment: organization-defined additional actions]: document the failure and resolution, troubleshoot, repair/restart the audit logging process, and report as incident if applicable *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.05 Audit Record Review, Analysis, and Reporting

> a\. Review and analyze system audit records [Assignment: organization-defined frequency] for indications and the potential impact of inappropriate or unusual activity.\
> b\. Report findings to organizational personnel or roles.\
> c\. Analyze and correlate audit records across different repositories to gain organization-wide situational awareness.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.5. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.5.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.03.05.a` [Assignment: organization-defined frequency]: at least weekly *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.06 Audit Record Reduction and Report Generation

> a\. Implement an audit record reduction and report generation capability that supports audit record review, analysis, reporting requirements, and after-the-fact investigations of incidents.\
> b\. Preserve the original content and time ordering of audit records.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.6. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.6.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.07 Time Stamps

> a\. Use internal system clocks to generate time stamps for audit records.\
> b\. Record time stamps for audit records that meet [Assignment: organization-defined granularity of time measurement] and that use Coordinated Universal Time (UTC), have a fixed local time offset from UTC, or include the local time offset as part of the time stamp.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.7. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.3.7.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.03.07.b` [Assignment: organization-defined granularity of time measurement]: a granularity of one (1) second or smaller *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.03.08 Protection of Audit Information

> a\. Protect audit information and audit logging tools from unauthorized access, modification, and deletion.\
> b\. Authorize access to management of audit logging functionality to only a subset of privileged users or roles.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.3.8; it also covers withdrawn 3.3.9. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.4 Configuration Management (CM)

#### 03.04.01 Baseline Configuration

> a\. Develop and maintain under configuration control, a current baseline configuration of the system.\
> b\. Review and update the baseline configuration of the system [Assignment: organization-defined frequency] and when system components are installed or modified.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.4.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.01.b` [Assignment: organization-defined frequency]: at least every 12 months and after any significant incidents or significant changes occur *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.02 Configuration Settings

> a\. Establish, document, and implement the following configuration settings for the system that reflect the most restrictive mode consistent with operational requirements: [Assignment: organization-defined configuration settings].\
> b\. Identify, document, and approve any deviations from established configuration settings.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.2; it also covers withdrawn 3.13.7. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.02.a` [Assignment: organization-defined configuration settings]: Apply the appropriate use of common security configurations available from the National Institute of Standards and Technology’s National Checklist Program (NCP) website (https://ncp.nist.gov/repository) and prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other unauthorized connection to resources in external networks. Document any deviations from the published standard or source document. *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.03 Configuration Change Control

> a\. Define the types of changes to the system that are configuration-controlled.\
> b\. Review proposed configuration-controlled changes to the system, and approve or disapprove such changes with explicit consideration for security impacts.\
> c\. Implement and document approved configuration-controlled changes to the system.\
> d\. Monitor and review activities associated with configuration-controlled changes to the system.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.3. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.4.3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.04 Impact Analyses

> a\. Analyze changes to the system to determine potential security impacts prior to change implementation.\
> b\. Verify that the security requirements for the system continue to be satisfied after the system changes have been implemented.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.4.4.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.05 Access Restrictions for Change

> Define, document, approve, and enforce physical and logical access restrictions associated with changes to the system.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.5. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.4.5.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.06 Least Functionality

> a\. Configure the system to provide only mission-essential capabilities.\
> b\. Prohibit or restrict use of the following functions, ports, protocols, connections, and services: [Assignment: organization-defined functions, ports, protocols, connections, and services].\
> c\. Review the system [Assignment: organization-defined frequency] to identify unnecessary or nonsecure functions, ports, protocols, connections, and services.\
> d\. Disable or remove functions, ports, protocols, connections, and services that are unnecessary or nonsecure.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.6; it also covers withdrawn 3.4.7, 3.13.7. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.06.b` [Assignment: organization-defined functions, ports, protocols, connections, and services]: {{odp.03_04_06_b}} *DoD gives guidance, not a value: Where feasible, organizations should limit component functionality to a single function per component. Organizations should consider removing unused or unnecessary software and disabling unused or unnecessary physical and logical ports and protocols to prevent unauthorized connection of components, transfer of information, and tunneling. Organizations should employ network scanning tools, intrusion detection and prevention systems, and end-point protection technologies, such as firewalls and host-based intrusion detection systems, to identify and prevent the use of prohibited functions, protocols, ports, and services. Least functionality should also be achieved as part of the fundamental design and development of the system.*
- `03.04.06.c` [Assignment: organization-defined frequency]: at least every 12 months, when any system functions, ports, protocols, or services changes are made, and after any significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.08 Authorized Software – Allow by Exception

> a\. Identify software programs authorized to execute on the system.\
> b\. Implement a deny-all, allow-by-exception policy for the execution of authorized software programs on the system.\
> c\. Review and update the list of authorized software programs [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.4.8; it also covers withdrawn 3.4.7, 3.4.9. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.08.c` [Assignment: organization-defined frequency]: at least quarterly *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.10 System Component Inventory

> a\. Develop and document an inventory of system components.\
> b\. Review and update the system component inventory [Assignment: organization-defined frequency].\
> c\. Update the system component inventory as part of installations, removals, and system updates.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.10.b` [Assignment: organization-defined frequency]: at least quarterly *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.11 Information Location

> a\. Identify and document the location of CUI and the system components on which the information is processed and stored.\
> b\. Document changes to the system or system component location where CUI is processed and stored.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.04.12 System and Component Configuration for High-Risk Areas

> a\. Issue systems or system components with the following configurations to individuals traveling to high-risk locations: [Assignment: organization-defined system configurations].\
> b\. Apply the following security requirements to the systems or components when the individuals return from travel: [Assignment: organization-defined security requirements].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.04.12.a` [Assignment: organization-defined system configurations]: a configuration that has no CUI or FCI stored on the system and prevents the processing, storing, and transmission of CUI and FCI, unless a specific exception is granted in writing by the Contracting Officer *(default, not yet confirmed)*
- `03.04.12.b` [Assignment: organization-defined security requirements]: examine the system for signs of physical tampering and take the appropriate actions, and then either purge and reimage all storage media or destroy the system *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.5 Identification and Authentication (IA)

#### 03.05.01 User Identification, Authentication, and Re-Authentication

> a\. Uniquely identify and authenticate system users, and associate that unique identification with processes acting on behalf of those users.\
> b\. Re-authenticate users when [Assignment: organization-defined circumstances or situations requiring re-authentication].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.05.01.b` [Assignment: organization-defined circumstances or situations requiring re-authentication]: roles, authenticators, or credentials change (including modification of user privilege); when security categories of systems change; when the execution of privileged functions occurs; and after a session termination *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.02 Device Identification and Authentication

> Uniquely identify and authenticate [Assignment: organization-defined devices or types of devices] before establishing a system connection.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.2.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.05.02` [Assignment: organization-defined devices or types of devices]: all devices for identification, where feasible for authentication, and document when not feasible *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.03 Multi-Factor Authentication

> Implement multi-factor authentication for access to privileged and non-privileged accounts.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.3. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.04 Replay-Resistant Authentication

> Implement replay-resistant authentication mechanisms for access to privileged and non-privileged accounts.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.4.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.05 Identifier Management

> a\. Receive authorization from organizational personnel or roles to assign an individual, group, role, service, or device identifier.\
> b\. Select and assign an identifier that identifies an individual, group, role, service, or device.\
> c\. Prevent the reuse of identifiers for [Assignment: organization-defined time period].\
> d\. Manage individual identifiers by uniquely identifying each individual as [Assignment: organization-defined characteristic identifying individual status].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.5. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.5.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.05.05.c` [Assignment: organization-defined time period]: at least ten (10) years *(default, not yet confirmed)*
- `03.05.05.d` [Assignment: organization-defined characteristic identifying individual status]: privileged or non-privileged users; contractors, foreign nationals, and/or non-organizational users *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.07 Password Management

> a\. Maintain a list of commonly-used, expected, or compromised passwords, and update the list [Assignment: organization-defined frequency] and when organizational passwords are suspected to have been compromised.\
> b\. Verify that passwords are not found on the list of commonly used, expected, or compromised passwords when users create or update passwords.\
> c\. Transmit passwords only over cryptographically protected channels.\
> d\. Store passwords in a cryptographically protected form.\
> e\. Select a new password upon first use after account recovery.\
> f\. Enforce the following composition and complexity rules for passwords: [Assignment: organization-defined composition and complexity rules].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.7; it also covers withdrawn 3.5.10. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.05.07.a` [Assignment: organization-defined frequency]: at least quarterly *(default, not yet confirmed)*
- `03.05.07.f` [Assignment: organization-defined composition and complexity rules]: 1) Must have a minimum length of 16 characters. 2) Contains a string of characters that does not include the user’s account name or full name. *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.11 Authentication Feedback

> Obscure feedback of authentication information during the authentication process.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.5.11. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.5.11.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.05.12 Authenticator Management

> a\. Verify the identity of the individual, group, role, service, or device receiving the authenticator as part of the initial authenticator distribution.\
> b\. Establish initial authenticator content for any authenticators issued by the organization.\
> c\. Establish and implement administrative procedures for initial authenticator distribution; for lost, compromised, or damaged authenticators; and for revoking authenticators.\
> d\. Change default authenticators at first use.\
> e\. Change or refresh authenticators [Assignment: organization-defined frequency] or when the following events occur: [Assignment: organization-defined events].\
> f\. Protect authenticator content from unauthorized disclosure and modification.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.05.12.e.01` [Assignment: organization-defined frequency]: never for passwords where MFA is employed, at least every five (5) years for hard tokens and identification badges, and at least every three (3) years for all other authenticators *(default, not yet confirmed)*
- `03.05.12.e.02` [Assignment: organization-defined events]: after a relevant security incident or any evidence of compromise or loss *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.6 Incident Response (IR)

#### 03.06.01 Incident Handling

> Implement an incident-handling capability that is consistent with the incident response plan and includes preparation, detection and analysis, containment, eradication, and recovery.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.6.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.6.1.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.06.02 Incident Monitoring, Reporting, and Response Assistance

> a\. Track and document system security incidents.\
> b\. Report suspected incidents to the organizational incident response capability within [Assignment: organization-defined time period].\
> c\. Report incident information to [Assignment: organization-defined authorities].\
> d\. Provide an incident response support resource that offers advice and assistance to system users on handling and reporting incidents.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.6.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.6.2.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.06.02.b` [Assignment: organization-defined time period]: near real time or as soon as practicable upon discovery *(default, not yet confirmed)*
- `03.06.02.c` [Assignment: organization-defined authorities]: all applicable personnel and entities as specified by the contract, and in accordance with any incident response plan notification procedures *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.06.03 Incident Response Testing

> Test the effectiveness of the incident response capability [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.6.3. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.6.3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.06.03` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.06.04 Incident Response Training

> a\. Provide incident response training to system users consistent with assigned roles and responsibilities:\
> 1\. Within [Assignment: organization-defined time period] of assuming an incident response role or responsibility or acquiring system access,\
> 2\. When required by system changes, and\
> 3\. [Assignment: organization-defined frequency] thereafter.\
> b\. Review and update incident response training content [Assignment: organization-defined frequency] and following [Assignment: organization-defined events].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.06.04.a.01` [Assignment: organization-defined time period]: ten (10) days for privileged users, thirty (30) days for all other roles *(default, not yet confirmed)*
- `03.06.04.a.03` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.06.04.b.01` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*
- `03.06.04.b.02` [Assignment: organization-defined events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.06.05 Incident Response Plan

> a\. Develop an incident response plan that:\
> 1\. Provides the organization with a roadmap for implementing its incident response capability,\
> 2\. Describes the structure and organization of the incident response capability,\
> 3\. Provides a high-level approach for how the incident response capability fits into the overall organization,\
> 4\. Defines reportable incidents,\
> 5\. Addresses the sharing of incident information, and\
> 6\. Designates responsibilities to organizational entities, personnel, or roles.\
> b\. Distribute copies of the incident response plan to designated incident response personnel (identified by name and/or by role) and organizational elements.\
> c\. Update the incident response plan to address system and organizational changes or problems encountered during plan implementation, execution, or testing.\
> d\. Protect the incident response plan from unauthorized disclosure.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.7 Maintenance (MA)

#### 03.07.04 Maintenance Tools

> a\. Approve, control, and monitor the use of system maintenance tools.\
> b\. Check media with diagnostic and test programs for malicious code before it is used in the system.\
> c\. Prevent the removal of system maintenance equipment containing CUI by verifying that there is no CUI on the equipment, sanitizing or destroying the equipment, or retaining the equipment within the facility.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.7.4; it also covers withdrawn 3.7.2. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.07.05 Nonlocal Maintenance

> a\. Approve and monitor nonlocal maintenance and diagnostic activities.\
> b\. Implement multi-factor authentication and replay resistance in the establishment of nonlocal maintenance and diagnostic sessions.\
> c\. Terminate session and network connections when nonlocal maintenance is completed.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.7.5. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.7.5.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.07.06 Maintenance Personnel

> a\. Establish a process for maintenance personnel authorization.\
> b\. Maintain a list of authorized maintenance organizations or personnel.\
> c\. Verify that non-escorted personnel who perform maintenance on the system possess the required access authorizations.\
> d\. Designate organizational personnel with required access authorizations and technical competence to supervise the maintenance activities of personnel who do not possess the required access authorizations.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.7.6; it also covers withdrawn 3.7.2. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.8 Media Protection (MP)

#### 03.08.01 Media Storage

> Physically control and securely store system media that contain CUI.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.8.1.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.02 Media Access

> Restrict access to CUI on system media to authorized personnel or roles.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.8.2.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.03 Media Sanitization

> Sanitize system media that contain CUI prior to disposal, release out of organizational control, or release for reuse.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.3; it also covers withdrawn 3.7.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.04 Media Marking

> Mark system media that contain CUI to indicate distribution limitations, handling caveats, and applicable CUI markings.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.8.4.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.05 Media Transport

> a\. Protect and control system media that contain CUI during transport outside of controlled areas.\
> b\. Maintain accountability of system media that contain CUI during transport outside of controlled areas.\
> c\. Document activities associated with the transport of system media that contain CUI.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.5. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.8.5.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.07 Media Use

> a\. Restrict or prohibit the use of [Assignment: organization-defined types of system media].\
> b\. Prohibit the use of removable system media without an identifiable owner.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.7; it also covers withdrawn 3.8.8. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.08.07.a` [Assignment: organization-defined types of system media]: any removable media not managed by or on behalf of the organization *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.08.09 System Backup – Cryptographic Protection

> a\. Protect the confidentiality of backup information.\
> b\. Implement cryptographic mechanisms to prevent the unauthorized disclosure of CUI at backup storage locations.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.8.9. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.8.9.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.9 Personnel Security (PS)

#### 03.09.01 Personnel Screening

> a\. Screen individuals prior to authorizing access to the system.\
> b\. Rescreen individuals in accordance with [Assignment: organization-defined conditions requiring rescreening].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.9.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.9.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.09.01.b` [Assignment: organization-defined conditions requiring rescreening]: an organizational policy requiring rescreening when there is a significant incident, or change in status, related to an individual *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.09.02 Personnel Termination and Transfer

> a\. When individual employment is terminated:\
> 1\. Disable system access within [Assignment: organization-defined time period],\
> 2\. Terminate or revoke authenticators and credentials associated with the individual, and\
> 3\. Retrieve security-related system property.\
> b\. When individuals are reassigned or transferred to other positions in the organization:\
> 1\. Review and confirm the ongoing operational need for current logical and physical access authorizations to the system and facility, and\
> 2\. Modify access authorization to correspond with any changes in operational need.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.9.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.9.2.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.09.02.a.01` [Assignment: organization-defined time period]: four (4) hours *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.10 Physical Protection (PE)

#### 03.10.01 Physical Access Authorizations

> a\. Develop, approve, and maintain a list of individuals with authorized access to the facility where the system resides.\
> b\. Issue authorization credentials for facility access.\
> c\. Review the facility access list [Assignment: organization-defined frequency].\
> d\. Remove individuals from the facility access list when access is no longer required.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.10.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.10.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.10.01.c` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.10.02 Monitoring Physical Access

> a\. Monitor physical access to the facility where the system resides to detect and respond to physical security incidents.\
> b\. Review physical access logs [Assignment: organization-defined frequency] and upon occurrence of [Assignment: organization-defined events or potential indications of events].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.10.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.10.2.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.10.02.b.01` [Assignment: organization-defined frequency]: at least every 45 days *(default, not yet confirmed)*
- `03.10.02.b.02` [Assignment: organization-defined events or potential indications of events]: significant, novel incidents, or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.10.06 Alternate Work Site

> a\. Determine alternate work sites allowed for use by employees.\
> b\. Employ the following security requirements at alternate work sites: [Assignment: organization-defined security requirements].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.10.6. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.10.6.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.10.06.b` [Assignment: organization-defined security requirements]: adequate security, comparable to organizational security requirements at the primary work site where practical, documented in policy, and covered by training *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.10.07 Physical Access Control

> a\. Enforce physical access authorizations at entry and exit points to the facility where the system resides by:\
> 1\. Verifying individual physical access authorizations before granting access to the facility and\
> 2\. Controlling ingress and egress with physical access control systems, devices, or guards.\
> b\. Maintain physical access audit logs for entry or exit points.\
> c\. Escort visitors, and control visitor activity.\
> d\. Secure keys, combinations, and other physical access devices.\
> e\. Control physical access to output devices to prevent unauthorized individuals from obtaining access to CUI.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none directly; it also covers withdrawn 3.10.3, 3.10.4, 3.10.5. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.10.08 Access Control for Transmission

> Control physical access to system distribution and transmission lines within organizational facilities.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.11 Risk Assessment (RA)

#### 03.11.01 Risk Assessment

> a\. Assess the risk (including supply chain risk) of unauthorized disclosure resulting from the processing, storage, or transmission of CUI.\
> b\. Update risk assessments [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.11.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.11.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.11.01.b` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.11.02 Vulnerability Monitoring and Scanning

> a\. Monitor and scan the system for vulnerabilities [Assignment: organization-defined frequency] and when new vulnerabilities affecting the system are identified.\
> b\. Remediate system vulnerabilities within [Assignment: organization-defined response times].\
> c\. Update system vulnerabilities to be scanned [Assignment: organization-defined frequency] and when new vulnerabilities are identified and reported.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.11.2; it also covers withdrawn 3.11.3. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.11.02.a` [Assignment: organization-defined frequency]: at least monthly, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*
- `03.11.02.b` [Assignment: organization-defined response times]: thirty (30) days from date of discovery for high-risk vulnerabilities (including both critical and high); 90 days from date of discovery for moderate-risk vulnerabilities; and 180 days from date of discovery for low-risk vulnerabilities *(default, not yet confirmed)*
- `03.11.02.c` [Assignment: organization-defined frequency]: no more than 24 hours prior to running the scans *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.11.04 Risk Response

> Respond to findings from security assessments, monitoring, and audits.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.12 Security Assessment and Monitoring (CA)

#### 03.12.01 Security Assessment

> Assess the security requirements for the system and its environment of operation [Assignment: organization-defined frequency] to determine if the requirements have been satisfied.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.12.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.12.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.12.01` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.12.02 Plan of Action and Milestones

> a\. Develop a plan of action and milestones for the system:\
> 1\. To document the planned remediation actions to correct weaknesses or deficiencies noted during security assessments and\
> 2\. To reduce or eliminate known system vulnerabilities.\
> b\. Update the existing plan of action and milestones based on the findings from:\
> 1\. Security assessments,\
> 2\. Audits or reviews, and\
> 3\. Continuous monitoring activities.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.12.2. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.12.2.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.12.03 Continuous Monitoring

> Develop and implement a system-level continuous monitoring strategy that includes ongoing monitoring and security assessments.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.12.3; it also covers withdrawn 3.4.9. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.12.05 Information Exchange

> a\. Approve and manage the exchange of CUI between the system and other systems using [Selection (one or more): interconnection security agreements; information exchange security agreements; memoranda of understanding or agreement; service-level agreements; user agreements; non-disclosure agreements; other types of agreements].\
> b\. Document interface characteristics, security requirements, and responsibilities for each system as part of the exchange agreements.\
> c\. Review and update the exchange agreements [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.12.05.a` [Selection (one or more): interconnection security agreements; information exchange security agreements; memoranda of understanding or agreement; service-level agreements; user agreements; nondisclosure agreements; other types of agreements]: requirements as described in the contract *(default, not yet confirmed)*
- `03.12.05.c` [Assignment: organization-defined frequency]: at least every 12 months *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.13 System and Communications Protection (SC)

#### 03.13.01 Boundary Protection

> a\. Monitor and control communications at external managed interfaces to the system and key internal managed interfaces within the system.\
> b\. Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.\
> c\. Connect to external systems only through managed interfaces that consist of boundary protection devices arranged in accordance with an organizational security architecture.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.1; it also covers withdrawn 3.13.5. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.04 Information in Shared System Resources

> Prevent unauthorized and unintended information transfer via shared system resources.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.4.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.06 Network Communications – Deny by Default – Allow by Exception

> Deny network communications traffic by default, and allow network communications traffic by exception.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.6. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.6.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.08 Transmission and Storage Confidentiality

> Implement cryptographic mechanisms to prevent the unauthorized disclosure of CUI during transmission and while in storage.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.8; it also covers withdrawn 3.8.6, 3.13.16. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.09 Network Disconnect

> Terminate the network connection associated with a communications session at the end of the session or after [Assignment: organization-defined time period] of inactivity.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.9. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.9.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.13.09` [Assignment: organization-defined time period]: no longer than 15 minutes *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.10 Cryptographic Key Establishment and Management

> Establish and manage cryptographic keys in the system in accordance with the following key management requirements: [Assignment: organization-defined requirements for key generation, distribution, storage, access, and destruction].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.10. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.10.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.13.10` [Assignment: organization-defined requirements for key generation, distribution, storage, access, and destruction]: {{odp.03_13_10}} *DoD gives guidance, not a value: At a minimum, establish a policy and procedure in line with the latest Cryptographic key management guidance*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.11 Cryptographic Protection

> Implement the following types of cryptography to protect the confidentiality of CUI: [Assignment: organization-defined types of cryptography].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.11. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.11.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.13.11` [Assignment: organization-defined types of cryptography]: FIPS Validated Cryptography (https://csrc.nist.gov/Projects/Cryptographic-Module-Validation-Program/Validated-Modules) *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.12 Collaborative Computing Devices and Applications

> a\. Prohibit the remote activation of collaborative computing devices and applications with the following exceptions: [Assignment: organization-defined exceptions where remote activation is to be allowed].\
> b\. Provide an explicit indication of use to users physically present at the devices.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.12. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.12.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.13.12.a` [Assignment: organization-defined exceptions where remote activation is to be allowed]: only as enumerated and justified in the System Security Plan before such remote activation occurs, and only when there are no other options, and the remote activation is operationally critical *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.13 Mobile Code

> a\. Define acceptable mobile code and mobile code technologies.\
> b\. Authorize, monitor, and control the use of mobile code.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.13. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.13.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.13.15 Session Authenticity

> Protect the authenticity of communications sessions.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.13.15. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.13.15.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.14 System and Information Integrity (SI)

#### 03.14.01 Flaw Remediation

> a\. Identify, report, and correct system flaws.\
> b\. Install security-relevant software and firmware updates within [Assignment: organization-defined time period] of the release of the updates.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.14.1. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.14.1.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.14.01.b` [Assignment: organization-defined time period]: thirty (30) days for high-risk flaws (including both critical and high), 90 days for moderate-risk flaws, and 180 days for low-risk flaws *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.14.02 Malicious Code Protection

> a\. Implement malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code.\
> b\. Update malicious code protection mechanisms as new releases are available in accordance with configuration management policies and procedures.\
> c\. Configure malicious code protection mechanisms to:\
> 1\. Perform scans of the system [Assignment: organization-defined frequency] and real-time scans of files from external sources at endpoints or system entry and exit points as the files are downloaded, opened, or executed; and\
> 2\. Block malicious code, quarantine malicious code, or take other mitigation actions in response to malicious code detection.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.14.2; it also covers withdrawn 3.14.4, 3.14.5. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.14.02.c.01` [Assignment: organization-defined frequency]: at least weekly *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.14.03 Security Alerts, Advisories, and Directives

> a\. Receive system security alerts, advisories, and directives from external organizations on an ongoing basis.\
> b\. Generate and disseminate internal system security alerts, advisories, and directives, as necessary.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.14.3. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.14.3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.14.06 System Monitoring

> a\. Monitor the system to detect:\
> 1\. Attacks and indicators of potential attacks and\
> 2\. Unauthorized connections.\
> b\. Identify unauthorized use of the system.\
> c\. Monitor inbound and outbound communications traffic to detect unusual or unauthorized activities or conditions.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.14.6; it also covers withdrawn 3.14.7. For this system's Rev 2 text, see the Rev 2 plan's narratives for those requirements.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.14.08 Information Management and Retention

> Manage and retain CUI within the system and CUI output from the system in accordance with applicable laws, Executive Orders, directives, regulations, policies, standards, guidelines, and operational requirements.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.15 Planning (PL)

#### 03.15.01 Policy and Procedures

> a\. Develop, document, and disseminate to organizational personnel or roles the policies and procedures needed to satisfy the security requirements for the protection of CUI.\
> b\. Review and update policies and procedures [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.15.01.b` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.15.02 System Security Plan

> a\. Develop a system security plan that:\
> 1\. Defines the constituent system components;\
> 2\. Identifies the information types processed, stored, and transmitted by the system;\
> 3\. Describes specific threats to the system that are of concern to the organization;\
> 4\. Describes the operational environment for the system and any dependencies on or connections to other systems or system components;\
> 5\. Provides an overview of the security requirements for the system;\
> 6\. Describes the safeguards in place or planned for meeting the security requirements;\
> 7\. Identifies individuals that fulfill system roles and responsibilities; and\
> 8\. Includes other relevant information necessary for the protection of CUI.\
> b\. Review and update the system security plan [Assignment: organization-defined frequency].\
> c\. Protect the system security plan from unauthorized disclosure.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** 3.12.4. For this system's Rev 2 text, see the Rev 2 plan's narrative for 3.12.4.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.15.02.b` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.15.03 Rules of Behavior

> a\. Establish rules that describe the responsibilities and expected behavior for system usage and protecting CUI.\
> b\. Provide rules to individuals who require access to the system.\
> c\. Receive a documented acknowledgement from individuals indicating that they have read, understand, and agree to abide by the rules of behavior before authorizing access to CUI and the system.\
> d\. Review and update the rules of behavior [Assignment: organization-defined frequency].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.15.03.d` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.16 System and Services Acquisition (SA)

#### 03.16.01 Security Engineering Principles

> Apply the following systems security engineering principles to the development or modification of the system and system components: [Assignment: organization-defined systems security engineering principles].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.16.01` [Assignment: organization-defined systems security engineering principles]: {{odp.03_16_01}} *DoD gives guidance, not a value: At a minimum, documentation that provides user and administrator guidance for the implementation and operation of controls. The level of detail required in such documentation should be based on the degree to which organizations depend on the capabilities, functions, or mechanisms to meet risk response expectations. Requirements can include mandated configuration settings that specify allowed functions, ports, protocols, and services. Acceptance criteria for systems, system components, and system services are defined in the same manner as the criteria for any organizational acquisition or procurement.*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.16.02 Unsupported System Components

> a\. Replace system components when support for the components is no longer available from the developer, vendor, or manufacturer.\
> b\. Provide options for risk mitigation or alternative sources for continued support for unsupported components that cannot be replaced.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.16.03 External System Services

> a\. Require the providers of external system services used for the processing, storage, or transmission of CUI to comply with the following security requirements: [Assignment: organization-defined security requirements].\
> b\. Define and document user roles and responsibilities with regard to external system services, including shared responsibilities with external service providers.\
> c\. Implement processes, methods, and techniques to monitor security requirement compliance by external service providers on an ongoing basis.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.16.03.a` [Assignment: organization-defined security requirements]: 1. For cloud service providers: (i) FedRAMP Authorized at the FedRAMP Moderate (or higher) baseline in accordance with the FedRAMP Marketplace; or (ii) meets security requirements established by the government equivalent to the FedRAMP Moderate (or higher) baseline. 2. All other external service providers must meet NIST SP 800-171 R2. *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

### 4.17 Supply Chain Risk Management (SR)

#### 03.17.01 Supply Chain Risk Management Plan

> a\. Develop a plan for managing supply chain risks associated with the research and development, design, manufacturing, acquisition, delivery, integration, operations, maintenance, and disposal of the system, system components, or system services.\
> b\. Review and update the supply chain risk management plan [Assignment: organization-defined frequency].\
> c\. Protect the supply chain risk management plan from unauthorized disclosure.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.17.01.b` [Assignment: organization-defined frequency]: at least every 12 months, or when there are significant incidents or significant changes to risks *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.17.02 Acquisition Strategies, Tools, and Methods

> Develop and implement acquisition strategies, contract tools, and procurement methods to identify, protect against, and mitigate supply chain risks.

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

#### 03.17.03 Supply Chain Requirements and Processes

> a\. Establish a process for identifying and addressing weaknesses or deficiencies in the supply chain elements and processes.\
> b\. Enforce the following security requirements to protect against supply chain risks to the system, system components, or system services and to limit the harm or consequences from supply chain-related events: [Assignment: organization-defined security requirements].

**Status:** pending (not yet proven on the Rev 3 reference implementation). **Evidence:** none yet.

**Implementation:** Pending. This requirement is not yet proven on the Rev 3 reference implementation, so this library does not yet describe an implementation.

**Rev 2 basis:** none; this requirement is new in Rev 3.

**Organization-defined parameters** (the DoD values are the defaults until the site confirms them):

- `03.17.03.b` [Assignment: organization-defined security requirements]: at a minimum, integrate Supply Chain Risk Management (SCRM) into acquisition/procurement policies, provide adequate SCRM resources, define the SCRM control baseline, establish processes to ensure suppliers disclose significant vulnerabilities and significant incidents *(default, not yet confirmed)*

**Site responsibility:** Describe how the site meets this requirement until this library's Rev 3 text is written.

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
| AC — Access Control | 16 | 0 | 0 | 0 |
| AT — Awareness and Training | 2 | 0 | 0 | 0 |
| AU — Audit and Accountability | 8 | 0 | 0 | 0 |
| CM — Configuration Management | 10 | 0 | 0 | 0 |
| IA — Identification and Authentication | 8 | 0 | 0 | 0 |
| IR — Incident Response | 5 | 0 | 0 | 0 |
| MA — Maintenance | 3 | 0 | 0 | 0 |
| MP — Media Protection | 7 | 0 | 0 | 0 |
| PS — Personnel Security | 2 | 0 | 0 | 0 |
| PE — Physical Protection | 5 | 0 | 0 | 0 |
| RA — Risk Assessment | 3 | 0 | 0 | 0 |
| CA — Security Assessment and Monitoring | 4 | 0 | 0 | 0 |
| SC — System and Communications Protection | 10 | 0 | 0 | 0 |
| SI — System and Information Integrity | 5 | 0 | 0 | 0 |
| PL — Planning | 3 | {{status.pl.met}} | {{status.pl.not_met}} | {{status.pl.unverified}} |
| SA — System and Services Acquisition | 3 | {{status.sa.met}} | {{status.sa.not_met}} | {{status.sa.unverified}} |
| SR — Supply Chain Risk Management | 3 | {{status.sr.met}} | {{status.sr.not_met}} | {{status.sr.unverified}} |
| **TOTAL** | **97** | **0** | **0** | **0** |

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

- NIST SP 800-171 Rev 3, Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations
- NIST SP 800-171A Rev 3, Assessing Security Requirements for Controlled Unclassified Information
- DoD Organization-Defined Parameters for NIST SP 800-171 Revision 3 (memo signed April 10, 2025)
- DoD Assessment Methodology for NIST SP 800-171
- The CyberHygiene Project appliance release record for the installed version (0.2.0)

### Appendix C: Supporting Documentation

- Site stick: locked cabinet, office 2

### Appendix D: Document Maintenance

This plan is generated from chp-templates 1.0.0 and then maintained by the System Owner. Change it
when the system changes; record each change in the Document Revision History; review it every
3 months.

### Appendix E: Defined Parameters

Rev 3's organization-defined parameters are stated with each requirement in Section 4. The site's other decisions:

| Parameter | Value |
|:---|:---|
| Review cycle (months) | 3 |
| Backup frequency | day |
| Restore test frequency | quarter |

*Add further lettered appendices below; nothing reads their order.*
