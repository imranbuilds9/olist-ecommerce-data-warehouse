
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

issues = Counter()
examples = {}

def record_issue(name, order_id):
    issues[name] += 1
    examples.setdefault(name, [])
    if len(examples[name]) < 5:
        examples[name].append(order_id)

total_orders = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_orders += 1
        order_id = row["order_id"].strip()
        times = {}

        for column in timestamp_columns:
            value = row[column].strip()
            times[column] = value if value else None

        parsed = {}

        for column, value in times.items():
            if value:
                try:
                    from datetime import datetime
                    parsed[column] = datetime.strptime(
                        value, "%Y-%m-%d %H:%M:%S"
                    )
                except ValueError:
                    record_issue("Invalid timestamp format", order_id)

        purchase = parsed.get("order_purchase_timestamp")
        approved = parsed.get("order_approved_at")
        carrier = parsed.get("order_delivered_carrier_date")
        delivered = parsed.get("order_delivered_customer_date")
        estimated = parsed.get("order_estimated_delivery_date")

        if purchase and approved and approved < purchase:
            record_issue("Approval before purchase", order_id)

        if approved and carrier and carrier < approved:
            record_issue("Carrier timestamp before approval", order_id)

        if carrier and delivered and delivered < carrier:
            record_issue("Delivery before carrier timestamp", order_id)

        if purchase and delivered and delivered < purchase:
            record_issue("Delivery before purchase", order_id)

        if purchase and estimated and estimated < purchase:
            record_issue("Estimated delivery before purchase", order_id)

print("Total orders checked:", total_orders)
print("\nTimestamp validation results:")

for name in [
    "Invalid timestamp format",
    "Approval before purchase",
    "Carrier timestamp before approval",
    "Delivery before carrier timestamp",
    "Delivery before purchase",
    "Estimated delivery before purchase",
]:
    print(f"{name}: {issues[name]}")

    if examples.get(name):
        print("  Example order IDs:", ", ".join(examples[name]))
