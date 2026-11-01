import csv

path = r"data\raw\olist_products_dataset.csv"

products = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if not row["product_weight_g"].strip():
            continue

        product = {
            "product_id": row["product_id"],
            "category": row["product_category_name"],
            "weight_g": float(row["product_weight_g"]),
            "length_cm": float(row["product_length_cm"]),
            "height_cm": float(row["product_height_cm"]),
            "width_cm": float(row["product_width_cm"])
        }

        products.append(product)


measurements = [
    "weight_g",
    "length_cm",
    "height_cm",
    "width_cm"
]

for field in measurements:

    print(f"\n{'=' * 60}")
    print(f"LOWEST 5 VALUES: {field}")
    print("=" * 60)

    for product in sorted(products, key=lambda x: x[field])[:5]:
        print(product)

    print(f"\nHIGHEST 5 VALUES: {field}")
    print("=" * 60)

    for product in sorted(
        products,
        key=lambda x: x[field],
        reverse=True
    )[:5]:
        print(product)