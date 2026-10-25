# chp-templates 1.1.0: release notes

**Released:** October 2026 · **Additive; replaces 1.0.1 as current.**

## Systems use Automated_Compliance's committed form

Systems are now described **one entry per system**, using the names Automated_Compliance already publishes:

    [system.srv1]
    kind = identity server
    in_boundary = yes
    operating_system = Rocky Linux 9
    administered_by = A. Person
    provider =

- **The boundary list is derived.** The renderer builds `{{systems.in_boundary}}` from every `system.<name>` whose
  `in_boundary` is yes, in profile order, as "name (kind, operating system)". The templates themselves still never
  loop.
- **The old list is deprecated, not removed.** Setting `systems.in_boundary` directly still works when a profile has no
  `system.<name>` entries. Per-system entries take priority when both are present.
- **`in_boundary` must be yes or no.** Anything else is an error that names the key.
- **The five `system.<name>.*` names are in `vocabulary.md`**, all tagged private because they are host inventory.

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
