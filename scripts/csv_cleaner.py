#!/usr/bin/env python3
"""
csv_cleaner.py

Clean/normalize CSV data for safer imports:
- trim whitespace
- normalize null-like values (null, n/a, -, etc.) to empty
- optional lowercasing for selected columns (e.g., email)
- optional phone cleanup (remove spaces, dashes, parentheses)

Output:
- out/clean.csv
- out/summary.txt
"""

import argparse
import csv
import os
import re
from pathlib import Path
from typing import Dict, List


NULL_LIKE = {"null", "none", "n/a", "na", "-", "--", "undefined", "nil"}


def normalize_value(val: str, to_lower: bool = False) -> str:
    if val is None:
        return ""
    v = val.strip()
    if v == "":
        return ""
    if v.strip().lower() in NULL_LIKE:
        return ""
    if to_lower:
        v = v.lower()
    return v


def clean_phone(val: str) -> str:
    """
    Keep digits and leading + if present. Removes separators and common noise.
    Examples:
      "(+54) 9 351-123-4567" -> "+5493511234567"
      "351 123 4567" -> "3511234567"
    """
    if val is None:
        return ""
    v = val.strip()
    if v == "":
        return ""
    # preserve leading + if exists
    plus = "+" if v.startswith("+") else ""
    digits = re.sub(r"\D+", "", v)
    return plus + digits if digits else ""


def parse_kv_list(items: List[str]) -> Dict[str, str]:
    """
    Parse mapping like: ["E-mail=email", "Teléfono=phone"]
    """
    mapping: Dict[str, str] = {}
    for it in items:
        if "=" not in it:
            raise ValueError(f"Invalid mapping '{it}'. Use FROM=TO format.")
        src, dst = it.split("=", 1)
        mapping[src.strip()] = dst.strip()
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean/normalize CSV for imports.")
    parser.add_argument("--input", required=True, help="Input CSV path")
    parser.add_argument("--output", default="out/clean.csv", help="Output CSV path")
    parser.add_argument(
        "--lower",
        default="",
        help="Comma-separated columns to lowercase (e.g., email,username)",
    )
    parser.add_argument(
        "--phone",
        default="",
        help="Comma-separated columns to clean as phone numbers (e.g., phone,telefono)",
    )
    parser.add_argument(
        "--rename",
        nargs="*",
        default=[],
        help="Optional header rename mappings: 'FROM=TO' (e.g., 'E-mail=email')",
    )

    args = parser.parse_args()

    lower_cols = {c.strip() for c in args.lower.split(",") if c.strip()}
    phone_cols = {c.strip() for c in args.phone.split(",") if c.strip()}
    rename_map = parse_kv_list(args.rename) if args.rename else {}

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned_rows = 0
    changed_cells = 0

    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no headers.")

        original_headers = list(reader.fieldnames)
        headers = [rename_map.get(h, h) for h in original_headers]

        with out_path.open("w", encoding="utf-8", newline="") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=headers)
            writer.writeheader()

            for row in reader:
                new_row: Dict[str, str] = {}
                for old_h, new_h in zip(original_headers, headers):
                    raw = row.get(old_h, "")

                    before = raw if raw is not None else ""
                    # normalize + optional lowercase
                    val = normalize_value(before, to_lower=(new_h in lower_cols))

                    # optional phone cleanup
                    if new_h in phone_cols:
                        val = clean_phone(val)

                    new_row[new_h] = val

                    if (before or "") != (val or ""):
                        changed_cells += 1

                writer.writerow(new_row)
                cleaned_rows += 1

    summary_path = out_path.parent / "summary.txt"
    summary_text = (
        f"Input: {in_path}\n"
        f"Output: {out_path}\n"
        f"Rows processed: {cleaned_rows}\n"
        f"Cells changed: {changed_cells}\n"
        f"Lowercased cols: {', '.join(sorted(lower_cols)) or '(none)'}\n"
        f"Phone-clean cols: {', '.join(sorted(phone_cols)) or '(none)'}\n"
        f"Rename map: {rename_map or '(none)'}\n"
    )
    summary_path.write_text(summary_text, encoding="utf-8")

    print("Done.")
    print(summary_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
