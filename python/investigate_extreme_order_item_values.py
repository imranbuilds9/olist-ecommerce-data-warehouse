
import csv
from decimal import Decimal

path = r"data\raw\olist_order_items_dataset.csv"

max_price = Decimal("6735.00")
max_freight = Decimal("409.68")

price_records = []
freight_records = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        price = Decimal(row["price"].strip())
        freight = Decimal(row["freight_value"].strip())

        if price == max_price:
            price_records.append(row)

        if freight == max_freight:
            freight_records.append(row)

print("RECORDS WITH MAXIMUM PRICE")
print("Matching records:", len(price_records))

for row in price_records:
    print(
        "Order:", row["order_id"],
        "| Item:", row["order_item_id"],
        "| Product:", row["product_id"],
        "| Seller:", row["seller_id"],
        "| Price:", row["price"],
        "| Freight:", row["freight_value"]
    )

print("\nRECORDS WITH MAXIMUM FREIGHT")
print("Matching records:", len(freight_records))

for row in freight_records:
    print(
        "Order:", row["order_id"],
        "| Item:", row["order_item_id"],
        "| Product:", row["product_id"],
        "| Seller:", row["seller_id"],
        "| Price:", row["price"],
        "| Freight:", row["freight_value"]
    )
