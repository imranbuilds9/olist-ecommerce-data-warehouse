import csv
from decimal import Decimal

path = r"data\raw\olist_order_items_dataset.csv"

ratios = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        price = Decimal(row["price"])
        freight = Decimal(row["freight_value"])

        ratio = (freight / price) * 100
        ratios.append(ratio)

ratios.sort()

count = len(ratios)

def percentile(data, p):
    index = round((p / 100) * (len(data) - 1))
    return data[index]

print("Total order items:", count)
print("Minimum ratio:", round(ratios[0], 2), "%")
print("Median ratio:", round(percentile(ratios, 50), 2), "%")
print("75th percentile:", round(percentile(ratios, 75), 2), "%")
print("90th percentile:", round(percentile(ratios, 90), 2), "%")
print("95th percentile:", round(percentile(ratios, 95), 2), "%")
print("99th percentile:", round(percentile(ratios, 99), 2), "%")
print("Maximum ratio:", round(ratios[-1], 2), "%")

print("\nRatio distribution:")

ranges = [
    (0, 5),
    (5, 10),
    (10, 20),
    (20, 30),
    (30, 50),
    (50, 100),
    (100, float("inf"))
]

for lower, upper in ranges:
    matching = [
        ratio for ratio in ratios
        if lower <= ratio < upper
    ]

    print(
        f"{lower}% to {upper if upper != float('inf') else 'above'}%:",
        len(matching)
    )