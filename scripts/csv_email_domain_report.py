import csv
from collections import Counter

INPUT_FILE = "emails.csv"     # CSV de entrada
EMAIL_COLUMN = "email"        # nombre de la columna
OUTPUT_FILE = "domain_report.csv"


def extract_domain(email):
    if "@" not in email:
        return None
    return email.split("@")[-1].lower().strip()


def main():
    domains = Counter()

    with open(INPUT_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        if EMAIL_COLUMN not in reader.fieldnames:
            print(f"Column '{EMAIL_COLUMN}' not found.")
            return

        for row in reader:
            email = row.get(EMAIL_COLUMN, "").strip()
            domain = extract_domain(email)
            if domain:
                domains[domain] += 1

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["domain", "count"])

        for domain, count in domains.most_common():
            writer.writerow([domain, count])

    print("Domain report generated:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
