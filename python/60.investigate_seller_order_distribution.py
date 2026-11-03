import pandas as pd

items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

# Count distinct orders per seller
seller_orders = (
    items.groupby("seller_id")["order_id"]
    .nunique()
    .reset_index(name="unique_orders")
)

print("========== SELLER ORDER DISTRIBUTION ==========")

print("\nTotal sellers:", len(seller_orders))

print("\nOrder count distribution:")
print(
    seller_orders["unique_orders"].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )
)

# Group sellers into order-volume bands
bins = [0, 10, 50, 100, 500, 1000, float("inf")]

labels = [
    "1-10 orders",
    "11-50 orders",
    "51-100 orders",
    "101-500 orders",
    "501-1000 orders",
    "1000+ orders"
]

seller_orders["order_band"] = pd.cut(
    seller_orders["unique_orders"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

print("\nSeller count by order-volume band:")
print(seller_orders["order_band"].value_counts().sort_index())

print("\nTop 10 sellers by distinct orders:")
print(
    seller_orders.sort_values(
        "unique_orders",
        ascending=False
    ).head(10).to_string(index=False)
)

print("\nBottom 10 sellers by distinct orders:")
print(
    seller_orders.sort_values(
        "unique_orders",
        ascending=True
    ).head(10).to_string(index=False)
)