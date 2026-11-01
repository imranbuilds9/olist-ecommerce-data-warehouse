
import csv
from collections import Counter

base = r"data\raw"

orders_path = base + r"\olist_orders_dataset.csv"
items_path = base + r"\olist_order_items_dataset.csv"

orders = {}

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        orders[row["order_id"].strip()] = row["order_status"].strip()

orders_with_items = set()

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        orders_with_items.add(row["order_id"].strip())

orders_without_items = set(orders) - orders_with_items

status_counts = Counter(
    orders[order_id]
    for order_id in orders_without_items
)

print("Orders without item records:", len(orders_without_items))
print("\nStatus breakdown:")

for status, count in sorted(status_counts.items()):
    print(f"{status}: {count}")

print("\nTotal accounted for:", sum(status_counts.values()))
