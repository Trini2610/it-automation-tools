# CSV Email Validator

Validates email addresses inside a CSV file and produces a clean output + a report of invalid emails.

## What it does
- Reads a CSV file (e.g., exported contacts or leads)
- Validates email format
- Generates:
  - a filtered CSV (valid / invalid depending on your config)
  - a report with invalid rows (line number + value)

## Expected input
A CSV that contains a column named one of:
- `email`
- `Email`
- `correo`
- `mail`

(If your script uses a specific column name, update this section accordingly.)

## Usage (example)
```bash
python scripts/csv_email_validator.py --input data/contacts.csv --output out/valid_emails.csv
