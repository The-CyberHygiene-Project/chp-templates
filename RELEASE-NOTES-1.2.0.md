# chp-templates 1.2.0: release notes

**Released:** October 2026 · **Additive; replaces 1.1.0 as current.**

## Contracts use Automated_Compliance's committed form

Contracts are now one entry per contract, using Automated_Compliance's published names: `contract.<n>.label`,
`agency_group`, `vehicle`, `information`, `clauses`, `required_revision`, `revision_basis` and `last_verified`. All
are tagged private.

- **The contract list is derived.** The renderer builds `{{contract.list}}` from those entries, in number order, as
  "label (clauses)". An entry without a label shows as "contract n".
- **The old list is deprecated, not removed.** Setting `contract.list` directly still works when a profile has no
  `contract.<n>` entries.

## Reserved names

`vocabulary.md` gains a **Reserved** section: 23 names from Automated_Compliance's draft vocabulary (more `decision.*`
values, `facts.*` switches, `site.*` addresses and `organization.owner_name`).
- **They keep the same names**, so the two systems never diverge.
- **A profile may set them now**, but no template uses them yet.
- **A template adopts one only when a section needs it**, and that release says so.

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
