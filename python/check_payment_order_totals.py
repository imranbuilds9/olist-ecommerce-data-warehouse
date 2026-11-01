
import csv
from collections import Counter, defaultdict
from decimal import Decimal

payments_path = r"data\raw\olist_order_payments_dataset.csv"
orders_path = r"data\raw\olist_orders_dataset.csv"

payment_totals = defaultdict(Decimal)
payment_counts = Counter()

with open(payments_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        order_id = row["order_id"].strip()
        value = Decimal(row["payment_value"].strip())

        payment_totals[order_id] += value
        payment_counts[order_id] += 1

orders_with_payments = set(payment_totals)

orders_with_multiple_payment_records = sum(
    1 for count in payment_counts.values() if count > 1
)

orders_without_payment_records = 0
total_orders = 0

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_orders += 1
        if row["order_id"].strip() not in orders_with_payments:
            orders_without_payment_records += 1

print("Total orders:", total_orders)
print("Orders with payment records:", len(orders_with_payments))
print("Orders without payment records:", orders_without_payment_records)
print("Orders with multiple payment records:", orders_with_multiple_payment_records)
print("Total payment records:", sum(payment_counts.values()))
print("Total of all payment values:", sum(payment_totals.values(), Decimal("0.00")))

print("\nFirst five orders with multiple payment records:")
shown = 0

for order_id, count in payment_counts.items():
    if count > 1:
        print(
            "order_id:", order_id,
            "| payment records:", count,
            "| payment total:", payment_totals[order_id]
        )
        shown += 1
        if shown == 5:
            break
