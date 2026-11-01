
import csv
from collections import Counter

path = r"data\raw\product_category_name_translation.csv"

keys = []
missing_keys = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        key = row["product_category_name"].strip()

        if not key:
            missing_keys += 1

        keys.append(key)

counts = Counter(keys)

duplicate_keys = {
    key: count
    for key, count in counts.items()
    if count > 1
}

print("Total translation rows:", len(keys))
print("Distinct category keys:", len(counts))
print("Duplicate category keys:", len(duplicate_keys))
print("Rows with missing category keys:", missing_keys)

if duplicate_keys:
    print("\nDuplicate keys:")
    for key, count in duplicate_keys.items():
        print(repr(key), "occurrences:", count)
