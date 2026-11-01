
import csv
from datetime import datetime

path = r"data\raw\olist_orders_dataset.csv"

checked = 0
examples = []

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        carrier_text = row["order_delivered_carrier_date"].strip()
        delivered_text = row["order_delivered_customer_date"].strip()

        if not carrier_text or not delivered_text:
            continue

        carrier = datetime.strptime(
            carrier_text, "%Y-%m-%d %H:%M:%S"
        )
        delivered = datetime.strptime(
            delivered_text, "%Y-%m-%d %H:%M:%S"
        )

        if delivered < carrier:
            checked += 1

            if len(examples) < 10:
                examples.append(row)

print("Orders with delivery before carrier timestamp:", checked)
print("\nFirst 10 examples:\n")

for row in examples:
    print("Order ID:", row["order_id"])
    print("Status:", row["order_status"])
    print("Purchase:", row["order_purchase_timestamp"])
    print("Approved:", row["order_approved_at"])
    print("Carrier:", row["order_delivered_carrier_date"])
    print("Delivered:", row["order_delivered_customer_date"])
    print("Estimated delivery:", row["order_estimated_delivery_date"])
    print("-" * 40)
