
import csv
from datetime import datetime
from collections import Counter

path = r"data\raw\olist_orders_dataset.csv"

issue_count = 0
status_counts = Counter()
examples = []

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        approved_text = row["order_approved_at"].strip()
        carrier_text = row["order_delivered_carrier_date"].strip()

        if not approved_text or not carrier_text:
            continue

        approved = datetime.strptime(
            approved_text, "%Y-%m-%d %H:%M:%S"
        )
        carrier = datetime.strptime(
            carrier_text, "%Y-%m-%d %H:%M:%S"
        )

        if carrier < approved:
            issue_count += 1
            status = row["order_status"].strip()
            status_counts[status] += 1

            if len(examples) < 10:
                examples.append(row)

print("Carrier-before-approval cases:", issue_count)
print("\nBreakdown by order status:")

for status, count in sorted(status_counts.items()):
    print(f"{status}: {count}")

print("\nFirst 10 examples:\n")

for row in examples:
    print("Order ID:", row["order_id"])
    print("Status:", row["order_status"])
    print("Purchase:", row["order_purchase_timestamp"])
    print("Approved:", row["order_approved_at"])
    print("Carrier:", row["order_delivered_carrier_date"])
    print("Delivered:", row["order_delivered_customer_date"])
    print("-" * 40)
