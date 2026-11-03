
import csv
from decimal import Decimal, InvalidOperation

path = r"data\raw\olist_order_items_dataset.csv"

total_rows = 0

fields = {
    "price": {
        "missing": 0,
        "invalid": 0,
        "zero": 0,
        "negative": 0,
        "positive": 0,
    },
    "freight_value": {
        "missing": 0,
        "invalid": 0,
        "zero": 0,
        "negative": 0,
        "positive": 0,
    },
}

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1

        for field, counts in fields.items():
            raw_value = row[field].strip()

            if not raw_value:
                counts["missing"] += 1
                continue

            try:
                value = Decimal(raw_value)

            except InvalidOperation:
                counts["invalid"] += 1
                continue

            if value == 0:
                counts["zero"] += 1

            elif value < 0:
                counts["negative"] += 1

            else:
                counts["positive"] += 1

print("Total order-item rows:", total_rows)

for field, counts in fields.items():
    print(f"\nField: {field}")

    for category, count in counts.items():
        print(f"{category.capitalize()}: {count}")
