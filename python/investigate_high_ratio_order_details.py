import csv

BASE = "data/raw/"

target_orders = {
    "c5bdd8ef3c0ec420232e668302179113",
    "3ee6513ae7ea23bdfab5b9ab60bffcb5",
    "6e864b3f0ec71031117ad4cf46b7f2a1",
    "fb265b2dc558a56445dfc48f8224e201",
    "d642656598ae928a250620315d19e87e",
    "8272b63d03f5f79c56e9e4120aec44ef"
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

orders_by_id = {r["order_id"]: r for r in orders}
customers_by_id = {r["customer_id"]: r for r in customers}
sellers_by_id = {r["seller_id"]: r for r in sellers}
products_by_id = {r["product_id"]: r for r in products}
translations_by_category = {
    r["product_category_name"]: r["product_category_name_english"]
    for r in translations
}

for order_id in sorted(target_orders):

    order = orders_by_id[order_id]
    customer = customers_by_id[order["customer_id"]]

    order_items = [
        r for r in items
        if r["order_id"] == order_id
    ]

    print("\n" + "=" * 70)
    print("ORDER:", order_id)
    print("Status:", order["order_status"])
    print("Purchase date:", order["order_purchase_timestamp"])

    print("\nCUSTOMER")
    print("City:", customer["customer_city"])
    print("State:", customer["customer_state"])

    total_price = 0
    total_freight = 0

    print("\nORDER ITEMS")

    for item in order_items:
        seller = sellers_by_id[item["seller_id"]]
        product = products_by_id[item["product_id"]]

        category = product["product_category_name"]
        english_category = translations_by_category.get(
            category, "Translation unavailable"
        )

        price = float(item["price"])
        freight = float(item["freight_value"])

        total_price += price
        total_freight += freight

        print("\nItem:", item["order_item_id"])
        print("Product:", item["product_id"])
        print("Category:", english_category)
        print("Price:", price)
        print("Freight:", freight)
        print("Weight (g):", product["product_weight_g"])
        print("Dimensions (cm):",
              product["product_length_cm"],
              "x", product["product_height_cm"],
              "x", product["product_width_cm"])

        print("Seller:", seller["seller_id"])
        print("Seller city:", seller["seller_city"])
        print("Seller state:", seller["seller_state"])

    print("\nORDER TOTALS")
    print("Number of items:", len(order_items))
    print("Total item price: R$", round(total_price, 2))
    print("Total freight: R$", round(total_freight, 2))
    print("Combined total: R$", round(total_price + total_freight, 2))