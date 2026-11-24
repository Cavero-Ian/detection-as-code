#!/usr/bin/env python3
"""True-positive test runner: each Sigma rule must detect its labeled sample.

Env vars:
  CHAINSAW          path to the chainsaw binary (default: "chainsaw" on PATH)
  CHAINSAW_MAPPING  path to sigma-event-logs-all.yml (required)
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = ROOT / "tests" / "cases.yml"


def count_hits(path: Path) -> int:
    """Count detections in Chainsaw JSON (array) or JSONL output."""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return 0
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return sum(1 for line in text.splitlines() if line.strip())
    if isinstance(data, list):
        return len(data)
    raise ValueError(f"Unexpected Chainsaw JSON shape: {type(data).__name__}")


def run_case(case: dict, chainsaw: str, mapping: str) -> int:
    rule = ROOT / case["rule"]
    sample = ROOT / case["sample"]
    for p in (rule, sample):
        if not p.exists():
            raise FileNotFoundError(p)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "hits.json"
        cmd = [chainsaw, "hunt", str(sample), "-s", str(rule),
               "--mapping", mapping, "--json", "-o", str(out)]
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout).strip())
        return count_hits(out) if out.exists() else 0


def main() -> int:
    chainsaw = os.environ.get("CHAINSAW", "chainsaw")
    mapping = os.environ.get("CHAINSAW_MAPPING")
    if not mapping or not Path(mapping).exists():
        print("ERROR: set CHAINSAW_MAPPING to sigma-event-logs-all.yml", file=sys.stderr)
        return 2

    cases = yaml.safe_load(CASES_FILE.read_text(encoding="utf-8"))["cases"]
    failures = 0
    for case in cases:
        lo = case.get("expected_min", 1)
        hi = case.get("expected_max")
        try:
            hits = run_case(case, chainsaw, mapping)
            ok = hits >= lo and (hi is None or hits <= hi)
            detail = f"hits={hits} expected_min={lo}" + (f" expected_max={hi}" if hi is not None else "")
        except Exception as exc:  # report and keep testing the other cases
            ok, detail = False, f"ERROR: {exc}"
        failures += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {case['id']}: {detail}")

    print(f"\n{len(cases) - failures}/{len(cases)} test cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
