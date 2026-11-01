
import csv
from decimal import Decimal

path = r"data\raw\olist_order_items_dataset.csv"

zero_freight_rows = []
affected_orders = set()

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        freight = Decimal(row["freight_value"].strip())

        if freight == 0:
            zero_freight_rows.append(row)
            affected_orders.add(row["order_id"])

print("Zero-freight rows:", len(zero_freight_rows))
print("Distinct affected orders:", len(affected_orders))

print("\nFirst 20 zero-freight records:\n")

for row in zero_freight_rows[:20]:
    print(
        "Order:", row["order_id"],
        "| Item:", row["order_item_id"],
        "| Product:", row["product_id"],
        "| Seller:", row["seller_id"],
        "| Price:", row["price"],
        "| Freight:", row["freight_value"]
    )
