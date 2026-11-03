
import csv
from collections import Counter

path = r"data\raw\olist_orders_dataset.csv"

statuses = Counter()
missing_statuses = 0
total_orders = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_orders += 1
        status = row["order_status"].strip()

        if not status:
            missing_statuses += 1
        else:
            statuses[status] += 1

print("Total orders:", total_orders)
print("Missing status values:", missing_statuses)
print("\nOrder status distribution:")

for status, count in sorted(statuses.items()):
    percentage = count / total_orders * 100
    print(f"{status}: {count} ({percentage:.2f}%)")

print("\nTotal counted statuses:", sum(statuses.values()))
