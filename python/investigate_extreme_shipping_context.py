import csv

BASE = "data/raw/"

target_order_ids = {
    "0812eb902a67711a1cb742b3cdaa65ae",
    "a77e1550db865202c56b19ddc6dc4d53"
}


def load_csv(filename):
    with open(BASE + filename, encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


orders = load_csv("olist_orders_dataset.csv")
customers = load_csv("olist_customers_dataset.csv")
sellers = load_csv("olist_sellers_dataset.csv")
products = load_csv("olist_products_dataset.csv")
items = load_csv("olist_order_items_dataset.csv")
translations = load_csv("product_category_name_translation.csv")

orders_by_id = {row["order_id"]: row for row in orders}
customers_by_id = {row["customer_id"]: row for row in customers}
sellers_by_id = {row["seller_id"]: row for row in sellers}
products_by_id = {row["product_id"]: row for row in products}
translations_by_category = {
    row["product_category_name"]: row["product_category_name_english"]
    for row in translations
}

for order_id in target_order_ids:
    order = orders_by_id[order_id]

    print("\n" + "=" * 65)
    print("ORDER:", order_id)
    print("Order status:", order["order_status"])
    print("Purchase timestamp:", order["order_purchase_timestamp"])

    customer = customers_by_id[order["customer_id"]]

    print("\nCUSTOMER LOCATION")
    print("Customer ZIP prefix:", customer["customer_zip_code_prefix"])
    print("Customer city:", customer["customer_city"])
    print("Customer state:", customer["customer_state"])

    matching_items = [
        row for row in items
        if row["order_id"] == order_id
    ]

    for item in matching_items:
        seller = sellers_by_id[item["seller_id"]]
        product = products_by_id[item["product_id"]]

        category = product["product_category_name"]
        english_category = translations_by_category.get(
            category, "No English translation available"
        )

        price = float(item["price"])
        freight = float(item["freight_value"])

        print("\nORDER ITEM")
        print("Item number:", item["order_item_id"])
        print("Product ID:", item["product_id"])
        print("Product category (Portuguese):", category)
        print("Product category (English):", english_category)
        print("Product weight (grams):", product["product_weight_g"])
        print("Product length (cm):", product["product_length_cm"])
        print("Product height (cm):", product["product_height_cm"])
        print("Product width (cm):", product["product_width_cm"])

        print("\nSELLER LOCATION")
        print("Seller ID:", seller["seller_id"])
        print("Seller ZIP prefix:", seller["seller_zip_code_prefix"])
        print("Seller city:", seller["seller_city"])
        print("Seller state:", seller["seller_state"])

        print("\nITEM AMOUNTS")
        print("Price: R$", item["price"])
        print("Freight: R$", item["freight_value"])
        print("Freight as percentage of price:",
              round((freight / price) * 100, 2), "%")