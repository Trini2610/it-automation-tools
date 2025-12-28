#!/usr/bin/env python3
"""
csv_column_mapper.py

Normalize/rename CSV column headers to a standard schema.

Outputs:
- out/normalized.csv
- out/column_mapping.json
"""

import argparse
import csv
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_SYNONYMS: Dict[str, List[str]] = {
    "email": ["email", "e-mail", "mail", "correo", "correo_electronico", "correo electronico", "e mail"],
    "phone": ["phone", "tel", "telefono", "teléfono", "cel", "celular", "mobile", "whatsapp", "nro tel", "nro telefono"],
    "first_name": ["nombre", "first name", "firstname", "nombres"],
    "last_name": ["apellido", "last name", "lastname", "apellidos"],
    "full_name": ["nombre y apellido", "nombre completo", "full name", "fullname"],
    "dni": ["dni", "documento", "doc", "nro documento", "número de documento", "numero documento"],
    "country": ["pais", "país", "country"],
    "city": ["ciudad", "city", "localidad"],
    "source": ["origen", "source", "fuente"],
}


def slugify(text: str) -> str:
    """Lowercase, remove accents, keep alnum + underscore, collapse spaces."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^\w\s-]", " ", text)          # remove weird punctuation
    text = re.sub(r"[\s\-]+", "_", text).strip("_") # spaces/dashes to underscore
    return text


def build_reverse_map(synonyms: Dict[str, List[str]]) -> Dict[str, str]:
    """Map each synonym -> canonical key"""
    rev = {}
    for canonical, syns in synonyms.items():
        for s in syns:
            rev[slugify(s)] = canonical
    return rev


def rename_headers(headers: List[str], rev_map: Dict[str, str]) -> Tuple[List[str], Dict[str, str]]:
    """
    Returns (new_headers, mapping old->new).
    If no match found, we keep slugified original.
    Handles collisions by appending _2, _3, etc.
    """
    mapping: Dict[str, str] = {}
    used: Dict[str, int] = {}
    new_headers: List[str] = []

    for h in headers:
        key = slugify(h)
        target = rev_map.get(key, key)  # canonical if known, else slugified original

        # Avoid duplicates in final headers
        if target in used:
            used[target] += 1
            target_final = f"{target}_{used[target]}"
        else:
            used[target] = 1
            target_final = target

        mapping[h] = target_final
        new_headers.append(target_final)

    return new_headers, mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize CSV column headers to a standard schema.")
    parser.add_argument("--input", "-i", required=True, help="Path to input CSV (e.g., data/input.csv)")
    parser.add_argument("--output", "-o", default="out/normalized.csv", help="Path to output CSV")
    parser.add_argument("--mapping", "-m", default="out/column_mapping.json", help="Path to mapping JSON log")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    map_path = Path(args.mapping)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.parent.mkdir(parents=True, exist_ok=True)

    rev_map = build_reverse_map(DEFAULT_SYNONYMS)

    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if not headers:
            raise ValueError("Input CSV has no header row.")

    # Re-read using DictReader so we can rewrite with new headers cleanly
    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        dict_reader = csv.DictReader(f)
        original_headers = dict_reader.fieldnames or []

        new_headers, mapping = rename_headers(original_headers, rev_map)

        # Build rows with renamed keys
        rows = []
        for row in dict_reader:
            new_row = {}
            for old_k, v in row.items():
                new_k = mapping.get(old_k, slugify(old_k))
                new_row[new_k] = v
            rows.append(new_row)

    # Write normalized CSV
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in new_headers})

    # Write mapping log
    with map_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"input": str(in_path), "output": str(out_path), "mapping": mapping},
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"OK ✅ Normalized CSV saved to: {out_path}")
    print(f"Mapping log saved to: {map_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
