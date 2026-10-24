# QiPR Software Identity and Publication Supplement

This append-only supplement closes a documentation gap in the canonical cold-start evidence publication. The original ZIP remains unchanged because its SHA3-512 digest and RFC 3161 timestamp are already public.

## Public records

- GitHub repository: https://github.com/evocyberreality/QiPR-evidence
- GitHub commit: https://github.com/evocyberreality/QiPR-evidence/commit/c9adb876cee041135e080611b642def333fd89dd
- GitHub release: https://github.com/evocyberreality/QiPR-evidence/releases/tag/v2026.10.22
- Zenodo DOI: https://doi.org/10.5281/zenodo.23577442
- Zenodo record: https://zenodo.org/records/23577442
- Canonical evidence: https://qreality.eu/q_paradigm/api/evidence/reproduction-cold-20261021T132500Z

## What this supplement establishes

`SOFTWARE_IDENTITY.json` places the canonical evidence archive, its manifest and TSA time, the GitHub publication, the Zenodo record, the public verifier, and the protected-core module hashes into one machine-readable record.

`PROTECTED_CORE_MANIFEST_PUBLIC.json` identifies the protected current implementation through plaintext and encrypted-module SHA3-512 digests without publishing the private source or encryption key.

## Important boundary

The 48-run cold reproduction disclosed a compatibility authorization shim. Therefore this supplement does **not** retroactively claim that all 48 runs were produced by the byte-identical current protected core. It identifies both records and their relationship without rewriting history.

The strongest future execution-to-binary proof requires a new certified run series whose start certificate records an executable, container or reproducible-build digest before execution and whose end certificate binds the same digest to the output.

## Erratum for the original archive

The original `EVIDENCE_FINGERPRINT_SHA3-512.txt` contains the stale manifest digest `305bf7a0…`. The actual manifest digest is `10eda5ff…`, as recorded by `AUDIT_STAMP.json` and verified by the RFC 3161 timestamp response. See `EVIDENCE_ERRATA.json`. The original timestamped archive remains unchanged; this correction is append-only.
