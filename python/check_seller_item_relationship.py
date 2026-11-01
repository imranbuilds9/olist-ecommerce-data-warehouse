
import csv

sellers_path = r"data\raw\olist_sellers_dataset.csv"
items_path = r"data\raw\olist_order_items_dataset.csv"

seller_ids = set()

with open(sellers_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        seller_id = row["seller_id"].strip()
        if seller_id:
            seller_ids.add(seller_id)

total_items = 0
missing_seller_ids = 0
unmatched_seller_references = 0

with open(items_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_items += 1
        seller_id = row["seller_id"].strip()

        if not seller_id:
            missing_seller_ids += 1
        elif seller_id not in seller_ids:
            unmatched_seller_references += 1

print("Seller records available:", len(seller_ids))
print("Order item rows checked:", total_items)
print("Order items with missing seller_id:", missing_seller_ids)
print("Order items referencing nonexistent sellers:", unmatched_seller_references)
