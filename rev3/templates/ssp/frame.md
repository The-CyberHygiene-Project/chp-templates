# SYSTEM SECURITY PLAN

## NIST SP 800-171 Rev 3 Compliance

{{organization.legal_name}} (doing business as {{organization.dba}})\
**System Name:** {{system.name}}\
**Domain:** {{site.domain}}\
**Version:** {{document.version}} **Date:** {{document.date}}\
**Classification:** {{document.classification}}

**Distribution Notice:** This document contains confidential details of {{organization.legal_name}}'s security
controls. Distribution is limited to the people named in Document Control and to assessors authorized by the System
Owner.

## DOCUMENT CONTROL

**Document Status:** {{document.status}}\
**Security Classification:** CONTROLLED UNCLASSIFIED INFORMATION (CUI)\
**Distribution:** Limited to authorized personnel only

| Name / Title | Role | Signature / Date |
|:---|:---|:---|
| {{roles.system_owner}} | System Owner | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |
| {{roles.security_officer}} | ISSO | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |

**Review Schedule:** every {{decision.review_cycle_months}} months, and upon any significant change to the system\
**Next Review Date:** {{document.next_review}}

### Document Revision History

| Version | Date | Author | Description |
|:---|:---|:---|:---|
| {{document.version}} | {{document.date}} | {{document.author}} | **Initial issue.** Generated from chp-templates {{templates.version}}. |

Add each later revision as a new row **above** the previous one (newest first). Use MM/DD/YYYY dates and begin the
description with a bold lead sentence.

## EXECUTIVE SUMMARY

### 1.1 Purpose

This System Security Plan documents the security requirements of NIST SP 800-171 Revision 2 as they are met for
**{{system.name}}**, which processes, stores and transmits Controlled Unclassified Information (CUI) for
{{organization.legal_name}}. It describes the system boundary, the operating environment, and how each requirement is
implemented, and it is the reference for the companion Plan of Action and Milestones (POA&M).

### 1.2 System Overview

{{system.name}} is built on the CyberHygiene Project appliance: an identity server and enrolled client workstations
installed from a signed installer image and configured from the site's own settings. Section 3 describes the
components; Section 4 describes each requirement's implementation, and states plainly where the site, not the appliance,
is responsible.

| Measure | Definition | Value |
|:---|:---|:---|
| **SPRS score** | The DoD Assessment Methodology score, on the basis the site's contracts require. Assessed {{assessment.sprs_date}}. **Basis:** {{assessment.sprs_basis}} | **{{assessment.sprs_score}}** |
| **Strict 800-171A objectives met** | Requirements for which **every** SP 800-171A Rev 3 assessment objective is satisfied, or not applicable with a stated reason; unweighted and not derived from SPRS. Assessed {{assessment.objectives_date}}. | **{{assessment.objectives_met}}/97** |

**POA&M reference:** {{poam.reference}} (the companion document; see Section 10).

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

{{contract.list | list}}

### 1.4 Key Findings

**Strengths:**

{{assessment.strengths | list}}

**Outstanding deficits** (each is an item in the POA&M):

{{assessment.deficits | list}}

### 1.5 Authorization

This plan is approved by the System Owner and the ISSO (see Authorization).

## 2. SYSTEM IDENTIFICATION

### 2.1 System Information

| Item | Value |
|:---|:---|
| System name | {{system.name}} |
| Domain | {{site.domain}} |
| Time zone | {{site.timezone}} |
| Operational status | {{system.status}} |

### 2.2 Organization Information

| Item | Value |
|:---|:---|
| Legal name | {{organization.legal_name}} |
| Doing business as | {{organization.dba}} |
| Location | {{organization.location}} |
| UEI | {{organization.uei}} |
| CAGE code | {{organization.cage}} |

### 2.3 Contact Information

| Role | Name | Contact |
|:---|:---|:---|
| System Owner | {{roles.system_owner}} | {{organization.owner_email}} |
| ISSO | {{roles.security_officer}} | {{organization.owner_email}} |
| System Administrator | {{roles.administrator}} | |

### 2.4 System Categorization

The system handles these categories of CUI:

{{scope.cui_types | list}}

### 2.5 System Boundary

{{scope.boundary_note}}

**Systems inside the boundary:**

{{systems.in_boundary | list}}

{{#if facts.has_outside_it_provider}}
**Outside IT provider:** the provider's access and the agreement that governs it are listed in Appendix C.
{{/if}}

## 3. SYSTEM DESCRIPTION

### 3.1 System Purpose and Functions

{{system.purpose}}

{{> arch}}

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

{{> controls}}

## 5. CONTINGENCY PLANNING (CP)

### System Backup

Backups are taken every {{decision.backup_frequency}}, and a restore is tested every
{{decision.restore_test_frequency}}. The appliance's recovery secrets (disk passphrases, the root console and boot-loader
passwords, the identity administrators' recovery passwords and the certificate authority's key) are held on the site
stick, which is stored as described in Appendix C. The site stick is not a backup of data.

### System Recovery

A failed host is reinstalled from the signed installer image and the site stick, then restored from backup. A host's
encrypted disk unlocks through its TPM; if the TPM binding is lost, the escrowed passphrase on the site stick unlocks it.

## 6. SECURITY POLICIES AND PROCEDURES

The policies and procedures that this plan relies on are maintained as separate documents:

{{policies.list | list}}

## 10. PLAN OF ACTION AND MILESTONES (POA&M)

Every requirement that is not fully met is tracked in the POA&M ({{poam.reference}}), with its weakness, milestones,
owner and scheduled completion date. The POA&M is reviewed every {{decision.review_cycle_months}} months.

## 11. IMPLEMENTATION METRICS

### Control Family Status

{{> family_status}}

## 12. CONCLUSION

{{assessment.conclusion}}

## AUTHORIZATION

By signing, the System Owner and the ISSO confirm that this plan describes the system as it is operated, and accept the
risk of the open items in the POA&M.

| Name / Title | Role | Signature / Date |
|:---|:---|:---|
| {{roles.system_owner}} | System Owner | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |
| {{roles.security_officer}} | ISSO | \_\_\_\_\_\_ Date: \_\_\_\_\_\_ |

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
- The CyberHygiene Project appliance release record for the installed version ({{system.appliance_version}})

### Appendix C: Supporting Documentation

{{supporting.documents | list}}

### Appendix D: Document Maintenance

This plan is generated from chp-templates {{templates.version}} and then maintained by the System Owner. Change it
when the system changes; record each change in the Document Revision History; review it every
{{decision.review_cycle_months}} months.

### Appendix E: Defined Parameters

Rev 3's organization-defined parameters are stated with each requirement in Section 4. The site's other decisions:

| Parameter | Value |
|:---|:---|
| Review cycle (months) | {{decision.review_cycle_months}} |
| Backup frequency | {{decision.backup_frequency}} |
| Restore test frequency | {{decision.restore_test_frequency}} |

*Add further lettered appendices below; nothing reads their order.*
