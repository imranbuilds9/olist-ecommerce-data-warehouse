
import csv

products_path = r"data\raw\olist_products_dataset.csv"
items_path = r"data\raw\olist_order_items_dataset.csv"

product_ids = set()

with open(products_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        product_id = row["product_id"].strip()
        if product_id:
            product_ids.add(product_id)

total_items = 0
missing_product_ids = 0
unmatched_product_references = 0

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_items += 1
        product_id = row["product_id"].strip()

        if not product_id:
            missing_product_ids += 1
        elif product_id not in product_ids:
            unmatched_product_references += 1

print("Product records available:", len(product_ids))
print("Order item rows checked:", total_items)
print("Order items with missing product_id:", missing_product_ids)
print("Order items referencing nonexistent products:", unmatched_product_references)
