
import csv

base = r"data\raw"

orders_path = base + r"\olist_orders_dataset.csv"
items_path = base + r"\olist_order_items_dataset.csv"

order_ids = set()

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_ids.add(row["order_id"].strip())

orders_with_items = set()

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        orders_with_items.add(row["order_id"].strip())

orders_without_items = sorted(order_ids - orders_with_items)

print("Total unique orders:", len(order_ids))
print("Orders with at least one item:", len(order_ids & orders_with_items))
print("Orders without item records:", len(orders_without_items))

if orders_without_items:
    print("\nFirst 10 orders without items:")
    for order_id in orders_without_items[:10]:
        print(order_id)
