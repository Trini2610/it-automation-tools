# CSV Email Domain Report

Generates a domain usage report from a CSV file containing email addresses.

## Description
This script reads a CSV file, extracts email domains, and creates a report with the number of occurrences per domain.

## Input
- CSV file with an `email` column

## Output
- `domain_report.csv` containing:
  - domain
  - count

## Example use cases
- Cleaning email databases
- Detecting corporate vs public email domains
- Data analysis before migrations or campaigns

## How to run
1. Place your CSV file in the same directory
2. Set the correct column name in the script
3. Run:
