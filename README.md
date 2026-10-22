# QiPR Evidence

**QiPR — Quantum inspirations Paradigm Reality**  
Author: Petr Schön — https://www.linkedin.com/in/cyberrealite/

This repository publishes the canonical cold-start evidence package for the QiPR local audit-simulator reproduction.

## Canonical evidence

- Endpoint: https://qreality.eu/q_paradigm/api/evidence/reproduction-cold-20261021T132500Z
- Archive: `evidence/evidence_reproduction_cold_20261021T132500Z_updated.zip`
- Archive SHA3-512: `e326e10900331ea0bc12ecb51269a34cd4008b7a8f1857d9819356b639b5e4739436ad8e5982bca6c4e686e59a158a2fe999ec438cb6a1c2f3d5193681500a90`
- Size: 5,189,987 bytes
- ZIP members: 256
- Manifest artifacts: 249
- Runs: 48
- Finished attempts: 48

The archive contains no private core and no private signing key. The legacy `d77264ae...` archive is not canonical and is not included here.

## Verification

```bash
python3 verify_evidence.py evidence/evidence_reproduction_cold_20261021T132500Z_updated.zip
```

Expected output includes `ALL OK 48/48` and the canonical archive hash. The verifier checks archive structure, manifest sizes and SHA3-512 digests, run outputs, certificate hash linkage and the 48 finished attempts.

## RFC 3161 timestamp

The manifest timestamp response is `evidence/manifest.tsr`. Its verification material is included as `evidence/cacert.pem`:

```bash
openssl ts -verify \
  -data evidence/PUBLIC_EVIDENCE_SUPPLEMENT_MANIFEST.json \
  -in evidence/manifest.tsr \
  -CAfile evidence/cacert.pem
```

Expected output: `Verification: OK`.

The timestamp establishes the existence and integrity of the manifest at the TSA time. It does not by itself establish scientific correctness or patent novelty.

## Permanent record

The published Zenodo record and DOI are:

- DOI: [10.5281/zenodo.23577442](https://doi.org/10.5281/zenodo.23577442)
- Record: https://zenodo.org/records/23577442

Use the DOI when citing or archiving this release. The GitHub repository and live evidence endpoint remain the verification sources for the same canonical archive.
