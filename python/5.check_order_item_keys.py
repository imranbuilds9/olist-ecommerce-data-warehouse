
import csv
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "data" / "raw" / "olist_order_items_dataset.csv"

keys = []
missing_keys = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = row["order_id"].strip()
        item_id = row["order_item_id"].strip()

        if not order_id or not item_id:
            missing_keys += 1

        keys.append((order_id, item_id))

counts = Counter(keys)
duplicate_keys = {
    key: count for key, count in counts.items() if count > 1
}

print("Total order-item rows:", len(keys))
print("Distinct order-item key combinations:", len(counts))
print("Duplicate key combinations:", len(duplicate_keys))
print("Rows with a missing key component:", missing_keys)

if duplicate_keys:
    print("\nFirst five duplicate keys:")
    for key, count in list(duplicate_keys.items())[:5]:
        print(key, "occurrences:", count)
