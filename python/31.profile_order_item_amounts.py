
import csv
from decimal import Decimal

path = r"data\raw\olist_order_items_dataset.csv"

prices = []
freight_values = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        prices.append(Decimal(row["price"].strip()))
        freight_values.append(
            Decimal(row["freight_value"].strip())
        )

for name, values in [
    ("price", prices),
    ("freight_value", freight_values),
]:
    print(f"\nField: {name}")
    print("Minimum:", min(values))
    print("Maximum:", max(values))
    print("Average:", sum(values) / len(values))
