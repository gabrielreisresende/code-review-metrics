import csv

def read_repositories(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row["full_name"] for row in reader]

def save_to_csv(data, csv_path):
    if not data:
        return
    keys = data[0].keys()
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
