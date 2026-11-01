
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_ids(filename, column):
    ids = set()

    with open(
        DATA_DIR / filename,
        encoding="utf-8-sig",
        newline=""
    ) as file:
        for row in csv.DictReader(file):
            value = row[column].strip()
            if value:
                ids.add(value)

    return ids


order_ids = load_ids("olist_orders_dataset.csv", "order_id")
product_ids = load_ids("olist_products_dataset.csv", "product_id")
seller_ids = load_ids("olist_sellers_dataset.csv", "seller_id")

missing_orders = set()
missing_products = set()
missing_sellers = set()
total_rows = 0

with open(
    DATA_DIR / "olist_order_items_dataset.csv",
    encoding="utf-8-sig",
    newline=""
) as file:
    for row in csv.DictReader(file):
        total_rows += 1

        if row["order_id"] not in order_ids:
            missing_orders.add(row["order_id"])

        if row["product_id"] not in product_ids:
            missing_products.add(row["product_id"])

        if row["seller_id"] not in seller_ids:
            missing_sellers.add(row["seller_id"])

print("Order-item rows checked:", total_rows)
print("Missing order references:", len(missing_orders))
print("Missing product references:", len(missing_products))
print("Missing seller references:", len(missing_sellers))

if missing_orders:
    print("Example missing order IDs:", list(missing_orders)[:5])

if missing_products:
    print("Example missing product IDs:", list(missing_products)[:5])

if missing_sellers:
    print("Example missing seller IDs:", list(missing_sellers)[:5])
