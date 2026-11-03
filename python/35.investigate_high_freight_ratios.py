import csv
from decimal import Decimal

path = r"data\raw\olist_order_items_dataset.csv"

records = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        price = Decimal(row["price"])
        freight = Decimal(row["freight_value"])

        ratio = (freight / price) * 100

        if ratio >= 100:
            records.append({
                "order_id": row["order_id"],
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "seller_id": row["seller_id"],
                "price": price,
                "freight": freight,
                "ratio": ratio
            })

records.sort(key=lambda x: x["ratio"], reverse=True)

print("Records with freight >= item price:", len(records))
print("\nTOP 10 HIGHEST FREIGHT-TO-PRICE RATIOS")

for record in records[:10]:
    print(
        "Order:", record["order_id"],
        "| Item:", record["order_item_id"],
        "| Product:", record["product_id"],
        "| Seller:", record["seller_id"],
        "| Price: R$", record["price"],
        "| Freight: R$", record["freight"],
        "| Ratio:", round(record["ratio"], 2), "%"
    )