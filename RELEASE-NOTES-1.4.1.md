# chp-templates 1.4.1: release notes

**Released:** November 2026 · **Additive; replaces 1.4.0 as current.** Placeholders unchanged: no name was added,
renamed or removed, so a profile that works with 1.4.0 works with 1.4.1.

## Rev 3 POA&M: the document server's rows

The Rev 3 POA&M now seeds **T-08 to T-16**, the CHP appliance's document-server limits that 1.4.0 added to the Rev 2
POA&M. The weakness, milestones, due date, owner and status are the same. The requirement numbers are translated with
`rev3/crosswalk.csv` (NIST's change analysis):

| Item | Rev 2 | Rev 3 |
|---|---|---|
| T-08 | 3.13.11 | 03.13.11 |
| T-09 | 3.4.8 | 03.04.08 |
| T-10 | 3.13.11, 3.1.5 | 03.01.05, 03.13.11 |
| T-11 | 3.14.1 | 03.14.01 |
| T-12 | 3.3.8, 3.3.1, 3.5.10 | 03.03.01, 03.03.08, 03.05.07 |
| T-13 | 3.3.8, 3.3.2 | 03.03.02, 03.03.08 |
| T-14 | 3.13.1, 3.1.3 | 03.01.03, 03.13.01 |
| T-15 | 3.1.1, 3.5.2 | 03.01.01, 03.05.02 |
| T-16 | 3.8.4 | 03.08.04 |

NIST withdrew 3.5.10 and folded it into 03.05.07.

Rev 3 content version **0.1.1**. Every Rev 3 control block is still *pending*. The Rev 2 library and the document
templates are unchanged.

## For a site

A site that uses the Rev 2 plan has nothing to do. A site that uses the Rev 3 plan regenerates its POA&M and confirms,
adapts or closes each new row, and sets `due_t08` to `due_t16` in `[poam]`.
