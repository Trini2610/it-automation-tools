# CSV Cleaner / Normalizer

Small utility to clean and normalize CSV data before importing into CRMs, databases or internal tools.

## What it does
- Trims whitespace in every cell
- Converts null-like values to empty (`null`, `n/a`, `-`, `undefined`, etc.)
- Optional: lowercases selected columns (e.g. `email`)
- Optional: cleans phone columns (keeps digits and optional leading `+`)
- Optional: renames headers with simple mappings

## Usage

### Basic
```bash
python scripts/csv_cleaner.py --input data/input.csv

Lowercase email + clean phone
python scripts/csv_cleaner.py --input data/input.csv --lower email --phone phone

Rename headers while cleaning
python scripts/csv_cleaner.py --input data/input.csv --rename "E-mail=email" "Teléfono=phone"

Output

out/clean.csv (cleaned file)

out/summary.txt (processing summary)

Typical IT support use cases

Clean messy exports before bulk imports

Normalize leads lists (email/phone)

Reduce errors caused by inconsistent formatting
