
import csv
from decimal import Decimal
from collections import Counter

orders_path = r"data\raw\olist_orders_dataset.csv"
payments_path = r"data\raw\olist_order_payments_dataset.csv"
items_path = r"data\raw\olist_order_items_dataset.csv"

payment_order_ids = set()

with open(payments_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        payment_order_ids.add(row["order_id"].strip())

items_by_order = Counter()
item_price_by_order = {}
freight_by_order = {}

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_id = row["order_id"].strip()
        items_by_order[order_id] += 1

        item_price_by_order[order_id] = (
            item_price_by_order.get(order_id, Decimal("0.00"))
            + Decimal(row["price"].strip())
        )

        freight_by_order[order_id] = (
            freight_by_order.get(order_id, Decimal("0.00"))
            + Decimal(row["freight_value"].strip())
        )

missing_payment_orders = []

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_id = row["order_id"].strip()

        if order_id not in payment_order_ids:
            missing_payment_orders.append(row)

print("Orders without payment records:", len(missing_payment_orders))

for row in missing_payment_orders:
    order_id = row["order_id"].strip()

    print("\nOrder ID:", order_id)
    print("Order status:", row["order_status"])
    print("Purchase timestamp:", row["order_purchase_timestamp"])
    print("Approval timestamp:", row["order_approved_at"])
    print("Number of item rows:", items_by_order[order_id])
    print("Item price total:", item_price_by_order.get(order_id, Decimal("0.00")))
    print("Freight total:", freight_by_order.get(order_id, Decimal("0.00")))
