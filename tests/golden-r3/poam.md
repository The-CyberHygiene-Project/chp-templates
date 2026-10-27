# PLAN OF ACTION AND MILESTONES (POA&M)

## NIST SP 800-171 Rev 3

**Organization:** Example Manufacturing LLC\
**System:** Example Parts CUI Enclave\
**Version:** 1.0 **Date:** 10/24/2026\
**Companion to:** the System Security Plan for Example Parts CUI Enclave\
**Classification:** CUI

## DOCUMENT CONTROL

| Version | Date | Author | Description |
|:---|:---|:---|:---|
| 1.0 | 10/24/2026 | Alex Example | **Initial issue.** Generated from chp-templates 1.0.0, with the appliance's known gaps seeded. |

Add each later revision as a new row **above** the previous one (newest first), using MM/DD/YYYY dates.

## HOW TO USE THIS POA&M

Each item records one requirement that is not fully met: the weakness, the plan to correct it, who owns it, and when it
is due. Review the open items every 3 months, and record each status change in Document
Control.

Items marked *"seeded by the template: confirm, adapt or close"* come from the CyberHygiene Project appliance's own
known limits. For each one, the site either confirms it applies, adapts it, or closes it with a stated reason.

## ITEMS

| ID | Revision | Requirement | Weakness | Milestones | Scheduled completion | Owner | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|
| T-01 | Rev 3 | 03.10.07 | The appliance keeps no record of physical access to its hosts. *Seeded by the template: confirm, adapt or close.* | Choose a physical access log (for example a room or rack sign-in log); start using it; review it monthly. | 01/31/2027 | Alex Example, Owner | Open |
| T-02 | Rev 3 | 03.05.07, 03.13.11 | The identity server's own cryptography runs outside the FIPS-validated module, although the hosts run in FIPS mode. *Seeded by the template: confirm, adapt or close.* | Record the risk decision (accept or remediate); track the upstream FIPS build option. | 01/31/2027 | Alex Example, Owner | Open |
| T-03 | Rev 3 | 03.13.08 | The site stick is not encrypted, yet it holds every host's recovery secrets. *Seeded by the template: confirm, adapt or close.* | Store and transport it under physical safeguards (sealed, locked, accompanied), or encrypt it; record each use. | 11/30/2026 | Alex Example, Owner | Open |
| T-04 | Rev 3 | 03.01.10, 03.01.11, 03.13.09 | This version of the appliance configures no session lock, session termination or idle network disconnect. *Seeded by the template: confirm, adapt or close.* | Configure the device lock (03.01.10.a: initiating a device lock after “at most 15 minutes” of inactivity and requiring the user to initiate a device lock before leaving the system unattended *(default, not yet confirmed)*), session termination and SSH idle timeout on every host; verify each. | 12/31/2026 | Sam Sample | Open |
| T-05 | Rev 3 | 03.01.01 | This version of the appliance does not disable inactive accounts. *Seeded by the template: confirm, adapt or close.* | Set the identity server's account policy; schedule an inactivity review (at most 90 days). | 12/31/2026 | Sam Sample | Open |
| T-07 | Rev 3 | 03.04.03 | If the site stick is removed before a host's first boot finishes, the first later use of the stick raises one file-integrity alert. *Seeded by the template: confirm, adapt or close.* | Leave the stick in until first boot finishes; accept the one alert with an audited approval if it occurs. | 11/30/2026 | Alex Example, Owner | Open |

T-06 (the fapolicyd SELinux denials) is not seeded: appliance update 0.2.0-update3 silences them, and the access is
still denied.

Add the site's own items below the seeded ones, numbered P-01, P-02 and so on.

## EVIDENCE FOR THE SEEDED ITEMS

The seeded items come from the appliance's release and proof records. Each item's evidence is named in the System
Security Plan's narrative for the same requirement.
