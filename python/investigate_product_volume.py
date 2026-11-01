import csv

path = r"data\raw\olist_products_dataset.csv"

products = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:

        dimensions = [
            row["product_length_cm"].strip(),
            row["product_height_cm"].strip(),
            row["product_width_cm"].strip()
        ]

        if any(value == "" for value in dimensions):
            continue

        length = float(row["product_length_cm"])
        height = float(row["product_height_cm"])
        width = float(row["product_width_cm"])

        volume = length * height * width

        products.append({
            "product_id": row["product_id"],
            "category": row["product_category_name"],
            "weight_g": row["product_weight_g"],
            "length_cm": length,
            "height_cm": height,
            "width_cm": width,
            "volume_cm3": volume
        })


print("Products with complete dimensions:", len(products))

print("\nTOP 10 LARGEST PRODUCTS BY VOLUME")
print("=" * 70)

for product in sorted(
    products,
    key=lambda x: x["volume_cm3"],
    reverse=True
)[:10]:
    print(product)


print("\nTOP 10 SMALLEST PRODUCTS BY VOLUME")
print("=" * 70)

for product in sorted(
    products,
    key=lambda x: x["volume_cm3"]
)[:10]:
    print(product)


print("\nPRODUCTS WITH ZERO WEIGHT AND COMPLETE DIMENSIONS")
print("=" * 70)

zero_weight = [
    product for product in products
    if product["weight_g"].strip()
    and float(product["weight_g"]) == 0
]

print("Count:", len(zero_weight))

for product in zero_weight:
    print(product)