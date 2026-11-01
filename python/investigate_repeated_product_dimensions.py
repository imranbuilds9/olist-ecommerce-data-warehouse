import csv
from collections import defaultdict

path = r"data\raw\olist_products_dataset.csv"

dimension_groups = defaultdict(list)

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:

        values = [
            row["product_length_cm"].strip(),
            row["product_height_cm"].strip(),
            row["product_width_cm"].strip(),
            row["product_weight_g"].strip()
        ]

        if any(value == "" for value in values):
            continue

        dimensions = (
            float(row["product_length_cm"]),
            float(row["product_height_cm"]),
            float(row["product_width_cm"])
        )

        product = {
            "product_id": row["product_id"],
            "category": row["product_category_name"],
            "weight_g": float(row["product_weight_g"])
        }

        dimension_groups[dimensions].append(product)


repeated_groups = {
    dimensions: products
    for dimensions, products in dimension_groups.items()
    if len(products) > 1
}

print("Distinct dimension combinations:", len(dimension_groups))
print("Repeated dimension combinations:", len(repeated_groups))

print("\nTOP 10 MOST FREQUENT DIMENSION COMBINATIONS")
print("=" * 70)

for dimensions, products in sorted(
    repeated_groups.items(),
    key=lambda item: len(item[1]),
    reverse=True
)[:10]:

    weights = [product["weight_g"] for product in products]

    print("\nDimensions (L, H, W):", dimensions)
    print("Products:", len(products))
    print("Minimum weight:", min(weights))
    print("Maximum weight:", max(weights))
    print("Distinct weights:", len(set(weights)))

    for product in products[:5]:
        print(product)


print("\nDIMENSION COMBINATION (16, 2, 11)")
print("=" * 70)

target = (16.0, 2.0, 11.0)

for product in dimension_groups.get(target, []):
    print(product)