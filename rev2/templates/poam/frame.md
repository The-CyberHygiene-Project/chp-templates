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

Add the site's own items below the seeded ones, numbered P-01, P-02 and so on.

## EVIDENCE FOR THE SEEDED ITEMS

The seeded items come from the appliance's release and proof records. Each item's evidence is named in the System
Security Plan's narrative for the same requirement.
