import csv
from collections import Counter

path = r"data\raw\olist_products_dataset.csv"

numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

total_rows = 0
product_ids = Counter()
category_counts = Counter()

stats = {
    column: {
        "missing": 0,
        "invalid": 0,
        "zero": 0,
        "negative": 0,
        "valid": 0,
        "min": None,
        "max": None
    }
    for column in numeric_columns
}

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1

        product_ids[row["product_id"]] += 1

        category = row["product_category_name"].strip()
        category_counts[category if category else "MISSING"] += 1

        for column in numeric_columns:
            value = row[column].strip()
            result = stats[column]

            if not value:
                result["missing"] += 1
                continue

            try:
                number = float(value)
            except ValueError:
                result["invalid"] += 1
                continue

            result["valid"] += 1

            if number == 0:
                result["zero"] += 1

            if number < 0:
                result["negative"] += 1

            if result["min"] is None or number < result["min"]:
                result["min"] = number

            if result["max"] is None or number > result["max"]:
                result["max"] = number


duplicate_product_ids = sum(
    count - 1
    for count in product_ids.values()
    if count > 1
)

print("\nTOTAL PRODUCT ROWS:", total_rows)
print("DISTINCT PRODUCT IDS:", len(product_ids))
print("DUPLICATE PRODUCT ID ROWS:", duplicate_product_ids)

print("\n--- PRODUCT CATEGORY COUNTS ---")

for category, count in category_counts.most_common():
    print(category, ":", count)

print("\n--- NUMERIC ATTRIBUTE PROFILE ---")

for column, result in stats.items():
    print("\nCOLUMN:", column)
    print("Missing:", result["missing"])
    print("Invalid:", result["invalid"])
    print("Zero:", result["zero"])
    print("Negative:", result["negative"])
    print("Valid:", result["valid"])
    print("Minimum:", result["min"])
    print("Maximum:", result["max"])