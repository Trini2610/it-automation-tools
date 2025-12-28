# CSV Column Mapper / Renamer

Normalize and rename CSV column headers into a clean, standard schema (email, phone, dni, etc.).
This is designed to prepare messy CSV exports before running other scripts (validator, domain report, duplicates).

## What it does
- Reads a CSV input
- Normalizes headers (lowercase, removes accents, spaces -> underscores)
- Maps common synonyms to canonical names (e.g., "Correo", "E-mail" -> `email`)
- Avoids header collisions automatically (`email`, `email_2`, ...)

## Output
- `out/normalized.csv` (clean headers)
- `out/column_mapping.json` (what changed -> what)

## Usage
```bash
python scripts/csv_column_mapper.py --input data/input.csv

Custom output paths:

python scripts/csv_column_mapper.py --input data/input.csv --output out/my_clean.csv --mapping out/map.json

Typical IT Support use cases

Cleaning leads/contacts exports before imports

Normalizing CRMs / forms / WhatsApp exports

Preparing a consistent input for validation and deduplication scripts
