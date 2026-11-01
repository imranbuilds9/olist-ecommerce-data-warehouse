import csv
from datetime import datetime
from collections import Counter

reviews_path = r"data\raw\olist_order_reviews_dataset.csv"
orders_path = r"data\raw\olist_orders_dataset.csv"

orders = {}

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        orders[row["order_id"]] = row["order_purchase_timestamp"]

fmt = "%Y-%m-%d %H:%M:%S"

total = 0
invalid_review_dates = 0
invalid_answer_dates = 0
missing_order_matches = 0

answer_before_creation = 0
creation_before_purchase = 0
same_day_creation = 0

examples = Counter()

with open(reviews_path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total += 1

        try:
            creation = datetime.strptime(
                row["review_creation_date"], fmt
            )
        except ValueError:
            invalid_review_dates += 1
            continue

        try:
            answer = datetime.strptime(
                row["review_answer_timestamp"], fmt
            )
        except ValueError:
            invalid_answer_dates += 1
            continue

        if answer < creation:
            answer_before_creation += 1

        purchase_value = orders.get(row["order_id"])

        if not purchase_value:
            missing_order_matches += 1
            continue

        try:
            purchase = datetime.strptime(purchase_value, fmt)
        except ValueError:
            continue

        if creation.date() < purchase.date():
            creation_before_purchase += 1

            if examples["creation_before_purchase"] < 5:
                print(
                    "\nCreation before purchase:",
                    "Order:", row["order_id"],
                    "| Purchase:", purchase,
                    "| Review creation:", creation
                )
                examples["creation_before_purchase"] += 1

        if creation.date() == purchase.date():
            same_day_creation += 1


print("\n" + "=" * 55)
print("REVIEW TIMESTAMP VALIDATION")
print("=" * 55)

print("Total review rows:", total)
print("Invalid review creation timestamps:", invalid_review_dates)
print("Invalid answer timestamps:", invalid_answer_dates)
print("Reviews without matching orders:", missing_order_matches)
print("Answer before creation:", answer_before_creation)
print("Review creation before purchase:", creation_before_purchase)
print("Review created on purchase date:", same_day_creation)