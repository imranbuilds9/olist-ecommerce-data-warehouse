
import csv
from decimal import Decimal
from collections import Counter

path = r"data\raw\olist_order_items_dataset.csv"

seller_counts = Counter()
product_counts = Counter()

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        freight = Decimal(row["freight_value"].strip())

        if freight == 0:
            seller_counts[row["seller_id"]] += 1
            product_counts[row["product_id"]] += 1

print("Distinct sellers with zero-freight items:",
      len(seller_counts))

print("Distinct products with zero-freight items:",
      len(product_counts))

print("\nTop 10 sellers by zero-freight item count:")

for seller, count in seller_counts.most_common(10):
    print(f"Seller: {seller} | Zero-freight items: {count}")

print("\nTop 10 products by zero-freight item count:")

for product, count in product_counts.most_common(10):
    print(f"Product: {product} | Zero-freight items: {count}")
