
import csv
from decimal import Decimal, InvalidOperation

path = r"data\raw\olist_order_payments_dataset.csv"

total_rows = 0
missing_payment_values = 0
invalid_payment_values = 0
zero_payment_values = 0
negative_payment_values = 0
positive_payment_values = 0
payment_types = set()

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_rows += 1

        payment_type = row["payment_type"].strip()
        if payment_type:
            payment_types.add(payment_type)

        raw_value = row["payment_value"].strip()

        if not raw_value:
            missing_payment_values += 1
            continue

        try:
            value = Decimal(raw_value)
        except InvalidOperation:
            invalid_payment_values += 1
            continue

        if not value.is_finite():
            invalid_payment_values += 1
        elif value == 0:
            zero_payment_values += 1
        elif value < 0:
            negative_payment_values += 1
        else:
            positive_payment_values += 1

print("Payment rows checked:", total_rows)
print("Missing payment values:", missing_payment_values)
print("Invalid numeric payment values:", invalid_payment_values)
print("Zero payment values:", zero_payment_values)
print("Negative payment values:", negative_payment_values)
print("Positive payment values:", positive_payment_values)
print("Distinct payment types:", len(payment_types))
print("Payment types:", sorted(payment_types))
