# chp-templates 1.3.1: release notes

**Released:** November 2026 · **Additive; replaces 1.3.0 as current.** Placeholders unchanged: no name was added,
renamed or removed, so a profile that works with 1.3.0 works with 1.3.1.

## Rev 2 narratives for the appliance's security add-on

The appliance's optional security add-on now covers more of these requirements. Each narrative says what the add-on
does and what the site still owns. All stay **partial**.

- **Malware scanning (YARA, appliance update 0.3.0-update1):**
  - **3.14.2:** new and changed files in the user and temporary folders are scanned every 5 minutes. A match alerts the
    administrator; nothing is moved or deleted.
  - **3.14.4:** the rules are a signed package, updated monthly through the appliance's repository.
  - **3.14.5:** a weekly scan covers every local file system. This requirement is now *partial* (it was *site*).
- **Network intrusion detection (Suricata, appliance update 0.4.0-update1):**
  - **3.14.6:** each host's own inbound and outbound traffic is watched with the Emerging Threats Open rules. It
    detects only; nothing is blocked. High severity reaches the administrator at once; medium goes into a daily
    summary.
  - **3.14.7:** Wazuh gathers audit records, account lockouts, monitor alerts and network alerts on the server.
  - **3.13.1:** Suricata watches and reports traffic, and does not block it.
- **Evidence:** the narratives cite the idm-assistant proof records `lab/security/PROOF-RECORD-Y1.md`,
  `PROOF-RECORD-S1.md` and (for 3.14.7) `PROOF-RECORD-W1.md`.

Rev 2 content version **1.2.3** (1.2.2 = YARA, 1.2.3 = Suricata). The Rev 3 library is unchanged (0.1.0, all
*pending*).

## For a site

Regenerate the SSP. If the security add-on is off, the narratives still describe it as optional; the site
responsibility lines then cover these requirements.

## Verifying this release

1. Check `SHA256SUMS.asc` against the project release key, `2DE0D71BF37D8F5E4201A590521276F43C908F8E`.
2. Run `shasum -a 256 -c SHA256SUMS`.
