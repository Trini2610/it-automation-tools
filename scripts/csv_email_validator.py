import csv
import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None

input_file = "input_emails.csv"
output_file = "valid_emails.csv"
invalid_file = "invalid_emails.csv"

with open(input_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    emails = [row[0] for row in reader if row]

valid_emails = []
invalid_emails = []

for email in emails:
    if is_valid_email(email):
        valid_emails.append([email])
    else:
        invalid_emails.append([email])

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(valid_emails)

with open(invalid_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(invalid_emails)

print(f"Valid emails: {len(valid_emails)}")
print(f"Invalid emails: {len(invalid_emails)}")
