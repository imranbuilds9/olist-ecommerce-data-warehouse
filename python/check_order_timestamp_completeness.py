
import csv
from collections import Counter

path = r"data\raw\olist_orders_dataset.csv"

timestamp_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

missing_counts = Counter()
status_missing_counts = Counter()
total_orders = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_orders += 1
        status = row["order_status"].strip()

        for column in timestamp_columns:
            if not row[column].strip():
                missing_counts[column] += 1
                status_missing_counts[(status, column)] += 1

print("Total orders:", total_orders)
print("\nMissing values by timestamp column:")

for column in timestamp_columns:
    count = missing_counts[column]
    percentage = count / total_orders * 100
    print(f"{column}: {count} ({percentage:.2f}%)")

print("\nMissing timestamp counts by order status:")

for (status, column), count in sorted(status_missing_counts.items()):
    print(f"{status} | {column}: {count}")
