#!/usr/bin/env python3
"""7 Days to Die V3.0 SandboxCode encoder/decoder.

No third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sandbox_options.json"


def load_options():
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing data file: {DATA_PATH}")
    by_id = {int(o["id"]): o for o in data}
    by_code = {o["code"].upper(): o for o in data}
    by_key = {}
    for o in data:
        for key in (o["property"], o["name"], o["code"], str(o["id"])):
            by_key[normalize_key(key)] = o
    return data, by_id, by_code, by_key


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def normalize_code(code: str) -> str:
    clean = re.sub(r"\s+", "", code or "").upper()
    return clean or "A"


def id_to_code(option_id: int) -> str:
    if option_id < 0 or option_id >= 26 * 26:
        raise ValueError("option id out of 2-letter A-Z range")
    return LETTERS[option_id // 26] + LETTERS[option_id % 26]


def code_to_id(two_letters: str) -> int:
    if len(two_letters) != 2 or any(ch not in LETTERS for ch in two_letters):
        raise ValueError(f"bad option code: {two_letters!r}")
    return (ord(two_letters[0]) - 65) * 26 + (ord(two_letters[1]) - 65)


def value_index_to_code(index: int) -> str:
    if index < 0 or index >= len(LETTERS):
        raise ValueError("value index out of A-Z range")
    return LETTERS[index]


def value_code_to_index(ch: str) -> int:
    if len(ch) != 1 or ch not in LETTERS:
        raise ValueError(f"bad value code: {ch!r}")
    return ord(ch) - 65


def parse_code(code: str, *, strict: bool = False):
    options, by_id, _by_code, _by_key = load_options()
    clean = normalize_code(code)
    if any(ch not in LETTERS for ch in clean):
        raise ValueError("SandboxCode may only contain A-Z letters and whitespace")
    version = clean[0]
    body = clean[1:]
    if len(body) % 3 != 0:
        raise ValueError("SandboxCode body length must be divisible by 3 after the version header")

    blocks = []
    for offset in range(0, len(body), 3):
        block = body[offset:offset + 3]
        pair = block[:2]
        value_code = block[2]
        option_id = code_to_id(pair)
        value_index = value_code_to_index(value_code)
        option = by_id.get(option_id)
        row = {
            "block": block,
            "option_id": option_id,
            "option_code": pair,
            "value_code": value_code,
            "value_index": value_index,
            "known": option is not None,
        }
        if option is None:
            row.update({
                "category": "Unknown",
                "name": f"Unknown option {pair}",
                "property": None,
                "type": None,
                "default": None,
                "value": None,
                "warning": "Option id is not in data/sandbox_options.json.",
            })
            if strict:
                raise ValueError(f"unknown option block: {block}")
        else:
            row.update({
                "category": option["category"],
                "name": option["name"],
                "property": option["property"],
                "type": option["type"],
                "default": option["default"],
            })
            if value_index >= len(option["values"]):
                row["value"] = None
                row["warning"] = "Value index is outside this option's known values."
                if strict:
                    raise ValueError(f"bad value for {pair}: {value_code}")
            else:
                row["value"] = option["values"][value_index]
                row["is_default"] = row["value"] == option["default"]
        blocks.append(row)
    return {"version": version, "code": clean, "blocks": blocks}


def find_value_index(option, raw_value: str) -> int:
    wanted = str(raw_value).strip()
    if wanted.endswith("%"):
        # Friendly input: 85% -> 0.85, 150% -> 1.5
        try:
            wanted = str(float(wanted[:-1].strip()) / 100.0).rstrip("0").rstrip(".")
        except ValueError:
            pass
    wanted_norm = wanted.lower()
    for i, value in enumerate(option["values"]):
        if value == wanted or value.lower() == wanted_norm:
            return i
        try:
            if float(value) == float(wanted):
                return i
        except ValueError:
            pass
    raise ValueError(
        f"bad value for {option['property']}: {raw_value!r}. "
        f"Allowed: {', '.join(option['values'])}"
    )


def encode_settings(settings: dict, *, version: str = "A", omit_defaults: bool = True) -> str:
    options, _by_id, _by_code, by_key = load_options()
    chosen = {}
    for key, raw_value in settings.items():
        option = by_key.get(normalize_key(str(key)))
        if option is None:
            raise ValueError(f"unknown setting: {key!r}")
        index = find_value_index(option, str(raw_value))
        value = option["values"][index]
        if omit_defaults and value == option["default"]:
            chosen.pop(option["code"], None)
        else:
            chosen[option["code"]] = value_index_to_code(index)
    body = []
    for option in options:
        value_code = chosen.get(option["code"])
        if value_code:
            body.append(option["code"] + value_code)
    return version + "".join(body)


def encode_decoded_json(data: dict, *, omit_defaults: bool = False) -> str:
    """Encode the JSON produced by decode --json.

    This preserves original block order, including unknown blocks, unless a known block is
    explicitly changed to its default and omit_defaults=True.
    """
    _options, by_id, _by_code, _by_key = load_options()
    version = str(data.get("version") or "A")[:1].upper()
    blocks = []
    if "blocks" in data:
        for row in data["blocks"]:
            pair = str(row.get("option_code") or row.get("block", "")[:2]).upper()
            option_id = int(row.get("option_id", code_to_id(pair)))
            option = by_id.get(option_id)
            raw_value = row.get("value")
            if option and raw_value is not None:
                index = find_value_index(option, str(raw_value))
                value = option["values"][index]
                if omit_defaults and value == option["default"]:
                    continue
                blocks.append(id_to_code(option_id) + value_index_to_code(index))
            else:
                block = str(row.get("block") or "").upper()
                if len(block) == 3 and all(ch in LETTERS for ch in block):
                    blocks.append(block)
                else:
                    value_code = str(row.get("value_code") or "A").upper()[:1]
                    blocks.append(id_to_code(option_id) + value_code)
        return version + "".join(blocks)

    # Also accept simple JSON objects: {"RangedDamage":"0.85", ...}
    return encode_settings(data, version=version, omit_defaults=True)


def print_human(decoded: dict) -> None:
    print(f"SandboxCode: {decoded['code']}")
    print(f"Version: {decoded['version']}")
    if not decoded["blocks"]:
        print("No non-default blocks. This is effectively the default code.")
        return
    print()
    print(f"{'Block':<5} {'Setting':<32} {'Property':<30} {'Value':<10} {'Default':<10}")
    print("-" * 92)
    for row in decoded["blocks"]:
        value = row.get("value") if row.get("value") is not None else "?"
        default = row.get("default") if row.get("default") is not None else "?"
        prop = row.get("property") or "?"
        name = row.get("name") or "?"
        print(f"{row['block']:<5} {name:<32.32} {prop:<30.30} {value:<10} {default:<10}")
        if row.get("warning"):
            print(f"      warning: {row['warning']}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Encode/decode 7 Days to Die V3.0 SandboxCode strings.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_decode = sub.add_parser("decode", help="Decode a SandboxCode")
    p_decode.add_argument("code", help="SandboxCode string, for example AAAJABJACJADJARFBNC")
    p_decode.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    p_decode.add_argument("--strict", action="store_true", help="Fail on unknown options or unknown value indexes")

    p_encode = sub.add_parser("encode", help="Encode settings into a SandboxCode")
    p_encode.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="Set option by property, name, 2-letter code, or id. May be repeated.")
    p_encode.add_argument("--json", metavar="PATH", help="Read settings JSON, or JSON output created by decode --json")
    p_encode.add_argument("--keep-defaults", action="store_true", help="Do not omit settings that equal known defaults when using --set")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "decode":
            decoded = parse_code(args.code, strict=args.strict)
            if args.json:
                print(json.dumps(decoded, indent=2, ensure_ascii=False))
            else:
                print_human(decoded)
            return 0

        if args.cmd == "encode":
            if args.json:
                src = Path(args.json)
                data = json.loads(src.read_text(encoding="utf-8"))
                print(encode_decoded_json(data, omit_defaults=not args.keep_defaults))
                return 0
            settings = {}
            for item in args.set:
                if "=" not in item:
                    raise ValueError(f"--set must use KEY=VALUE format: {item!r}")
                key, value = item.split("=", 1)
                settings[key.strip()] = value.strip()
            print(encode_settings(settings, omit_defaults=not args.keep_defaults))
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
