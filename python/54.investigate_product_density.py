import csv

path = r"data\raw\olist_products_dataset.csv"

products = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:

        values = [
            row["product_weight_g"].strip(),
            row["product_length_cm"].strip(),
            row["product_height_cm"].strip(),
            row["product_width_cm"].strip()
        ]

        if any(value == "" for value in values):
            continue

        weight = float(row["product_weight_g"])
        length = float(row["product_length_cm"])
        height = float(row["product_height_cm"])
        width = float(row["product_width_cm"])

        volume = length * height * width

        if volume == 0:
            continue

        density = weight / volume

        products.append({
            "product_id": row["product_id"],
            "category": row["product_category_name"],
            "weight_g": weight,
            "volume_cm3": volume,
            "density_g_cm3": density
        })


print("Products analyzed:", len(products))

print("\nTOP 10 HIGHEST WEIGHT-TO-VOLUME RATIOS")
print("=" * 70)

for product in sorted(
    products,
    key=lambda x: x["density_g_cm3"],
    reverse=True
)[:10]:
    print(product)


print("\nTOP 10 LOWEST WEIGHT-TO-VOLUME RATIOS")
print("=" * 70)

for product in sorted(
    products,
    key=lambda x: x["density_g_cm3"]
)[:10]:
    print(product)