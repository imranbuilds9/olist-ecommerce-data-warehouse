
import csv

base = r"data\raw"

orders_path = base + r"\olist_orders_dataset.csv"
items_path = base + r"\olist_order_items_dataset.csv"
payments_path = base + r"\olist_order_payments_dataset.csv"

orders = {}

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        orders[row["order_id"].strip()] = row

orders_with_items = set()

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        orders_with_items.add(row["order_id"].strip())

payment_counts = {}

with open(payments_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_id = row["order_id"].strip()
        payment_counts[order_id] = payment_counts.get(order_id, 0) + 1

print("Orders without items in unusual statuses:\n")

for order_id, row in orders.items():
    status = row["order_status"].strip()

    if order_id not in orders_with_items and status in {
        "created", "invoiced", "shipped"
    }:
        print("Order ID:", order_id)
        print("Status:", status)
        print("Purchase timestamp:", row["order_purchase_timestamp"])
        print("Approved timestamp:", row["order_approved_at"])
        print("Carrier timestamp:", row["order_delivered_carrier_date"])
        print("Delivered timestamp:", row["order_delivered_customer_date"])
        print("Payment records:", payment_counts.get(order_id, 0))
        print("-" * 40)
