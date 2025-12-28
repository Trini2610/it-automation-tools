# CSV Duplicates Finder

Detecta filas duplicadas en un CSV según una o varias columnas clave (por ejemplo: email, teléfono, DNI, ID).

## What it does
- Separa el archivo en:
  - `out/duplicates.csv`: filas que pertenecen a duplicados
  - `out/unique.csv`: filas únicas
  - `out/summary.txt`: resumen con conteos

## Requirements
- Python 3.10+ (funciona en 3.8+ también)

## Usage

### Example 1: Duplicados por email
```bash
python scripts/csv_duplicates_finder.py --input data/input.csv --keys email

### Example 2: Duplicados por email + teléfono (clave compuesta)

python scripts/csv_duplicates_finder.py --input data/input.csv --keys email,phone

### Example 3: Comparación sin distinguir mayúsculas/minúsculas

Output

out/duplicates.csv

out/unique.csv

out/summary.txt

Typical IT Support use cases

Bases con clientes repetidos

Leads duplicados por mail/teléfono

Usuarios repetidos por identificador

Limpieza previa a importaciones masivas
