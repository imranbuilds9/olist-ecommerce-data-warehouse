
import csv
from collections import Counter, defaultdict
from decimal import Decimal

path = r"data\raw\olist_order_payments_dataset.csv"

zero_payment_types = Counter()
zero_orders = defaultdict(list)

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        value = Decimal(row["payment_value"].strip())

        if value == 0:
            payment_type = row["payment_type"].strip()
            order_id = row["order_id"].strip()

            zero_payment_types[payment_type] += 1
            zero_orders[order_id].append({
                "payment_sequential": row["payment_sequential"],
                "payment_type": payment_type,
                "payment_installments": row["payment_installments"],
                "payment_value": row["payment_value"]
            })

print("Zero-value payment types:")
for payment_type, count in zero_payment_types.items():
    print(f"{payment_type}: {count}")

print("\nOrders containing zero-value payments:", len(zero_orders))

print("\nZero-value payment records:")
for order_id, payments in zero_orders.items():
    for payment in payments:
        print(
            "order_id:", order_id,
            "| payment_sequential:", payment["payment_sequential"],
            "| payment_type:", payment["payment_type"],
            "| installments:", payment["payment_installments"],
            "| payment_value:", payment["payment_value"]
        )
