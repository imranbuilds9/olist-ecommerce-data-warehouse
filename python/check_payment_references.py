
import csv

base = r"data\raw"

orders_path = base + r"\olist_orders_dataset.csv"
payments_path = base + r"\olist_order_payments_dataset.csv"

order_ids = set()

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_ids.add(row["order_id"].strip())

total_payments = 0
missing_order_refs = 0
examples = []

with open(payments_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_payments += 1
        order_id = row["order_id"].strip()

        if order_id not in order_ids:
            missing_order_refs += 1

            if len(examples) < 5:
                examples.append(order_id)

print("Unique order IDs:", len(order_ids))
print("Payment rows checked:", total_payments)
print("Payments with missing order references:", missing_order_refs)

if examples:
    print("Example missing order IDs:", examples)
