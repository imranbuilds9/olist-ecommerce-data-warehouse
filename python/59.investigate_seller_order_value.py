import pandas as pd

items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")

# Calculate seller performance at order level
seller_order = (
    items.groupby(["seller_id", "order_id"])
    .agg(
        order_items=("order_item_id", "count"),
        order_product_value=("price", "sum"),
        order_freight=("freight_value", "sum")
    )
    .reset_index()
)

# Aggregate order-level results by seller
seller_metrics = (
    seller_order.groupby("seller_id")
    .agg(
        unique_orders=("order_id", "count"),
        total_items=("order_items", "sum"),
        total_product_sales=("order_product_value", "sum"),
        average_order_value=("order_product_value", "mean"),
        average_items_per_order=("order_items", "mean")
    )
    .reset_index()
)

# Add seller location
seller_metrics = seller_metrics.merge(
    sellers[["seller_id", "seller_city", "seller_state"]],
    on="seller_id",
    how="left"
)

print("========== SELLER ORDER VALUE ANALYSIS ==========")

print("\nTotal seller-order combinations:", len(seller_order))
print("Total sellers:", len(seller_metrics))

print("\nOverall average product value per seller-order:")

print(
    round(
        seller_order["order_product_value"].mean(),
        2
    )
)

print("\nSeller average order value distribution:")

print(
    seller_metrics["average_order_value"].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )
)

print("\nTop 10 sellers by average order value:")

print(
    seller_metrics.sort_values(
        "average_order_value",
        ascending=False
    )[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "unique_orders",
            "average_order_value",
            "average_items_per_order"
        ]
    ].head(10).to_string(index=False)
)

print("\nBottom 10 sellers by average order value:")

print(
    seller_metrics.sort_values(
        "average_order_value",
        ascending=True
    )[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "unique_orders",
            "average_order_value",
            "average_items_per_order"
        ]
    ].head(10).to_string(index=False)
)

print("\nOrders containing multiple items from the same seller:")

multi_item_orders = seller_order[
    seller_order["order_items"] > 1
]

print("Seller-order combinations:", len(multi_item_orders))
print("Total items in these combinations:", multi_item_orders["order_items"].sum())

print("\nReconciliation:")
print("Original order items:", len(items))
print("Aggregated seller items:", seller_metrics["total_items"].sum())
print(
    "Item count matches:",
    len(items) == seller_metrics["total_items"].sum()
)