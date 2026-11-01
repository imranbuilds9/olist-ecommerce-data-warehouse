
import csv
from collections import Counter

path = r"data\raw\olist_order_payments_dataset.csv"

keys = []
missing_keys = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_id = row["order_id"].strip()
        payment_sequential = row["payment_sequential"].strip()

        if not order_id or not payment_sequential:
            missing_keys += 1

        keys.append((order_id, payment_sequential))

counts = Counter(keys)

duplicate_keys = {
    key: count
    for key, count in counts.items()
    if count > 1
}

print("Total payment rows:", len(keys))
print("Distinct key combinations:", len(counts))
print("Duplicate key combinations:", len(duplicate_keys))
print("Rows with missing key components:", missing_keys)

if duplicate_keys:
    print("\nFirst five duplicate keys:")
    for key, count in list(duplicate_keys.items())[:5]:
        print(key, "occurrences:", count)
