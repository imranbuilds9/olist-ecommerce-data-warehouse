import csv

path = r"data\raw\olist_products_dataset.csv"

missing_measurements = []
zero_weight_products = []
missing_descriptions = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:

        weight = row["product_weight_g"].strip()
        length = row["product_length_cm"].strip()
        height = row["product_height_cm"].strip()
        width = row["product_width_cm"].strip()

        name_length = row["product_name_lenght"].strip()
        description_length = row["product_description_lenght"].strip()
        photos = row["product_photos_qty"].strip()

        product = {
            "product_id": row["product_id"],
            "category": row["product_category_name"],
            "weight": weight,
            "length": length,
            "height": height,
            "width": width,
            "name_length": name_length,
            "description_length": description_length,
            "photos": photos
        }

        if not weight or not length or not height or not width:
            missing_measurements.append(product)

        if weight and float(weight) == 0:
            zero_weight_products.append(product)

        if not name_length or not description_length or not photos:
            missing_descriptions.append(product)


print("\nPRODUCTS WITH MISSING PHYSICAL MEASUREMENTS:",
      len(missing_measurements))

for product in missing_measurements:
    print(product)


print("\nPRODUCTS WITH ZERO WEIGHT:",
      len(zero_weight_products))

for product in zero_weight_products:
    print(product)


print("\nPRODUCTS WITH MISSING DESCRIPTIVE METADATA:",
      len(missing_descriptions))

print("FIRST 5 EXAMPLES:")

for product in missing_descriptions[:5]:
    print(product)