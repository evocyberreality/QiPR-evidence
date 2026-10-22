#!/usr/bin/env python3
"""Verify the QiPR cold-start evidence archive (structure, hashes and 48 runs)."""
from __future__ import annotations
import hashlib, io, json, re, sys, urllib.request, zipfile
from pathlib import Path

URL_PREFIX = "https://"

def read_source(source: str) -> tuple[bytes, str]:
    if source.startswith(URL_PREFIX):
        with urllib.request.urlopen(source, timeout=30) as r:
            return r.read(), source
    p = Path(source)
    if p.is_dir():
        import shutil, tempfile
        fd, name = tempfile.mkstemp(suffix=".zip")
        import os
        os.close(fd)
        shutil.make_archive(name[:-4], "zip", p)
        data = Path(name).read_bytes()
        Path(name).unlink(missing_ok=True)
        return data, str(p)
    return p.read_bytes(), str(p)

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_evidence.py <zip-or-url>", file=sys.stderr)
        return 2
    data, source = read_source(sys.argv[1])
    errors = []
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception as exc:
        print(f"FAIL: invalid ZIP: {exc}", file=sys.stderr); return 1
    names = z.namelist()
    roots = sorted({n.split("/", 1)[0] for n in names if "/" in n})
    root = roots[0] if len(roots) == 1 else ""
    def find(rel: str) -> str | None:
        exact = [n for n in names if n == rel]
        if exact: return exact[0]
        pref = root + "/" + rel if root else rel
        return pref if pref in names else None
    mn = find("PUBLIC_EVIDENCE_SUPPLEMENT_MANIFEST.json")
    if not mn:
        errors.append("manifest missing")
    else:
        manifest = json.loads(z.read(mn))
        for item in manifest.get("artifacts", []):
            rel = item["path"]; n = find(rel)
            if not n: errors.append(f"manifest artifact missing: {rel}"); continue
            b = z.read(n)
            if len(b) != item["bytes"]: errors.append(f"size mismatch: {rel}")
            if hashlib.sha3_512(b).hexdigest() != item["sha3_512"]:
                errors.append(f"hash mismatch: {rel}")
    run_re = re.compile(r"^" + re.escape(root + "/evidence/runs/" if root else "evidence/runs/") + r"([^/]+)/([^/]+)/([0-9]+)/run_output\.json$")
    runs = []
    for n in names:
        m = run_re.match(n)
        if m: runs.append((m.group(1), m.group(2), m.group(3), n))
    for contract, policy, repeat, out_name in runs:
        base = out_name.rsplit("/", 1)[0]
        def get(file): return base + "/" + file
        try:
            out = json.loads(z.read(out_name)); info = json.loads(z.read(get("run_info.json")))
            start = json.loads(z.read(get("certificate_start.json"))); end = json.loads(z.read(get("certificate_end.json")))
            if out.get("status") != "PASS" or info.get("status") != "PASS": errors.append(f"not PASS: {contract}/{policy}/{repeat}")
            if info.get("output_sha3_512") != hashlib.sha3_512(z.read(out_name)).hexdigest(): errors.append(f"run_info output hash mismatch: {contract}/{policy}/{repeat}")
            if end.get("run_id") != f"{contract}/{policy}/{repeat}": errors.append(f"certificate run_id mismatch: {contract}/{policy}/{repeat}")
            if end.get("output_sha3_512") != hashlib.sha3_512(z.read(out_name)).hexdigest(): errors.append(f"certificate output hash mismatch: {contract}/{policy}/{repeat}")
            if start.get("run_id") != end.get("run_id"): errors.append(f"certificate pair mismatch: {contract}/{policy}/{repeat}")
        except KeyError as exc:
            errors.append(f"missing run artifact {base}/{exc}")
        except Exception as exc:
            errors.append(f"invalid run {base}: {exc}")
    attempts = find("evidence/attempts.jsonl")
    attempt_records = [json.loads(x) for x in z.read(attempts).splitlines() if x.strip()] if attempts else []
    # The complete log records both attempt_started and attempt_finished. The
    # reproducible run count is the finished PASS records.
    attempt_count = sum(1 for x in attempt_records if x.get("event") == "attempt_finished")
    if len(runs) != 48: errors.append(f"expected 48 run outputs, found {len(runs)}")
    if attempt_count != 48: errors.append(f"expected 48 finished attempts, found {attempt_count}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s) in {source}")
        for e in errors[:20]: print(" -", e)
        return 1
    print(f"ALL OK 48/48: {source}")
    print(f"archive_sha3_512={hashlib.sha3_512(data).hexdigest()}")
    print(f"zip_members={len(names)} manifest_artifacts={manifest.get('artifact_count', 'n/a')} attempts={attempt_count}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

