
import csv

base = r"data\raw"

products_path = base + r"\olist_products_dataset.csv"
translations_path = base + r"\product_category_name_translation.csv"

product_categories = set()
missing_product_categories = 0

with open(products_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        category = row["product_category_name"].strip()

        if not category:
            missing_product_categories += 1
        else:
            product_categories.add(category)

translated_categories = set()

with open(translations_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        category = row["product_category_name"].strip()

        if category:
            translated_categories.add(category)

untranslated = sorted(product_categories - translated_categories)
unused_translations = sorted(translated_categories - product_categories)

print("Distinct non-empty product categories:", len(product_categories))
print("Products with missing category values:", missing_product_categories)
print("Categories with translations:", len(translated_categories))
print("Product categories without translations:", len(untranslated))
print("Translation categories not used by products:", len(unused_translations))

if untranslated:
    print("\nFirst 20 untranslated categories:")
    for category in untranslated[:20]:
        print(category)

if unused_translations:
    print("\nFirst 20 translation categories not used by products:")
    for category in unused_translations[:20]:
        print(category)
