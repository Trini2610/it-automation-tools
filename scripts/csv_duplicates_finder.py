#!/usr/bin/env python3
"""
csv_duplicates_finder.py

Find duplicate rows in a CSV based on one or multiple key columns.
Outputs:
- out/duplicates.csv  -> rows that are part of duplicates
- out/unique.csv      -> rows that are not duplicates
- out/summary.txt     -> simple summary
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import Counter
from pathlib import Path
from typing import List, Tuple


def read_csv(path: Path, delimiter: str = ",") -> Tuple[List[str], List[dict]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row (field names).")
        rows = list(reader)
        return reader.fieldnames, rows


def write_csv(path: Path, fieldnames: List[str], rows: List[dict], delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def normalize(value: str, case_insensitive: bool) -> str:
    v = (value or "").strip()
    return v.lower() if case_insensitive else v


def build_key(row: dict, keys: List[str], case_insensitive: bool) -> Tuple[str, ...]:
    return tuple(normalize(row.get(k, ""), case_insensitive) for k in keys)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect duplicates in a CSV by key column(s).")
    parser.add_argument("--input", required=True, help="Path to input CSV (e.g., data/input.csv)")
    parser.add_argument("--keys", required=True, help="Comma-separated key columns (e.g., email or email,phone)")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default: ,)")
    parser.add_argument("--case-insensitive", action="store_true", help="Compare keys case-insensitively")
    parser.add_argument("--outdir", default="out", help="Output directory (default: out)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 2

    key_cols = [k.strip() for k in args.keys.split(",") if k.strip()]
    if n
