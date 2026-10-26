# PLAN OF ACTION AND MILESTONES (POA&M)

## NIST SP 800-171 Rev 3

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
| T-01 | Rev 3 | 03.10.07 | The appliance keeps no record of physical access to its hosts. *Seeded by the template: confirm, adapt or close.* | Choose a physical access log (for example a room or rack sign-in log); start using it; review it monthly. | {{poam.due_t01}} | {{roles.security_officer}} | Open |
| T-02 | Rev 3 | 03.05.07, 03.13.11 | The identity server's own cryptography runs outside the FIPS-validated module, although the hosts run in FIPS mode. *Seeded by the template: confirm, adapt or close.* | Record the risk decision (accept or remediate); track the upstream FIPS build option. | {{poam.due_t02}} | {{roles.security_officer}} | Open |
| T-03 | Rev 3 | 03.13.08 | The site stick is not encrypted, yet it holds every host's recovery secrets. *Seeded by the template: confirm, adapt or close.* | Store and transport it under physical safeguards (sealed, locked, accompanied), or encrypt it; record each use. | {{poam.due_t03}} | {{roles.security_officer}} | Open |
| T-04 | Rev 3 | 03.01.10, 03.01.11, 03.13.09 | This version of the appliance configures no session lock, session termination or idle network disconnect. *Seeded by the template: confirm, adapt or close.* | Configure the device lock (03.01.10.a: {{odp.03_01_10_a}}), session termination and SSH idle timeout on every host; verify each. | {{poam.due_t04}} | {{roles.administrator}} | Open |
| T-05 | Rev 3 | 03.01.01 | This version of the appliance does not disable inactive accounts. *Seeded by the template: confirm, adapt or close.* | Set the identity server's account policy; schedule an inactivity review ({{odp.03_01_01_f_02}}). | {{poam.due_t05}} | {{roles.administrator}} | Open |
| T-07 | Rev 3 | 03.04.03 | If the site stick is removed before a host's first boot finishes, the first later use of the stick raises one file-integrity alert. *Seeded by the template: confirm, adapt or close.* | Leave the stick in until first boot finishes; accept the one alert with an audited approval if it occurs. | {{poam.due_t07}} | {{roles.security_officer}} | Open |

T-06 (the fapolicyd SELinux denials) is not seeded: appliance update 0.2.0-update3 silences them, and the access is
still denied.

Add the site's own items below the seeded ones, numbered P-01, P-02 and so on.

## EVIDENCE FOR THE SEEDED ITEMS

The seeded items come from the appliance's release and proof records. Each item's evidence is named in the System
Security Plan's narrative for the same requirement.
