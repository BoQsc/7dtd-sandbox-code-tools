#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
TOOL = ROOT / "sandbox_code.py"
SAMPLE = "AAAGABGACGADGARJAMJBUEBHIBOACDACVDCFBCHCCOHDAGDKKEHKFFAETA"
ADVENTURER = "AAAJABJACJADJARFBNC"


def run(*args: str) -> str:
    proc = subprocess.run([PY, str(TOOL), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    return proc.stdout.strip()


def main() -> int:
    assert run("encode") == "A"
    assert run("encode", "--set", "RangedDamage=0.85", "--set", "BiomeProgression=False") == "AAAGCDA"
    decoded = json.loads(run("decode", SAMPLE, "--json"))
    assert decoded["version"] == "A"
    assert decoded["blocks"][0]["property"] == "RangedDamage"
    assert decoded["blocks"][0]["value"] == "0.85"
    assert any(row.get("property") == "IncomingDamage" and row.get("value") == "1.5" for row in decoded["blocks"])
    assert any((not row["known"]) and row["block"] == "EHK" for row in decoded["blocks"])

    tmp = ROOT / "examples" / "sample_decoded.json"
    tmp.write_text(json.dumps(decoded, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    assert run("encode", "--json", str(tmp), "--keep-defaults") == SAMPLE

    adventurer = json.loads(run("decode", ADVENTURER, "--json"))
    assert run("encode", "--json", str(write_tmp("adventurer_decoded.json", adventurer)), "--keep-defaults") == ADVENTURER
    print("OK: all tests passed")
    return 0


def write_tmp(name: str, data: dict) -> Path:
    path = ROOT / "examples" / name
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    raise SystemExit(main())
