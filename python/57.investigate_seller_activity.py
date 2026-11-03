import pandas as pd

sellers_path = "data/raw/olist_sellers_dataset.csv"
items_path = "data/raw/olist_order_items_dataset.csv"

sellers = pd.read_csv(sellers_path)
items = pd.read_csv(items_path)

print("========== SELLER ACTIVITY ANALYSIS ==========")

# Basic counts
print("\nTotal sellers:", len(sellers))
print("Total order items:", len(items))

# Aggregate order-item activity by seller
seller_activity = (
    items.groupby("seller_id")
    .agg(
        total_order_items=("order_id", "count"),
        unique_orders=("order_id", "nunique"),
        total_product_sales=("price", "sum"),
        total_freight=("freight_value", "sum")
    )
    .reset_index()
)

# Include sellers with no order-item activity
seller_analysis = sellers.merge(
    seller_activity,
    on="seller_id",
    how="left"
)

# Fill activity counts and sales for inactive sellers
activity_columns = [
    "total_order_items",
    "unique_orders",
    "total_product_sales",
    "total_freight"
]

seller_analysis[activity_columns] = (
    seller_analysis[activity_columns].fillna(0)
)

# Seller activity counts
active_sellers = (
    seller_analysis["total_order_items"] > 0
).sum()

inactive_sellers = (
    seller_analysis["total_order_items"] == 0
).sum()

print("\nActive sellers:", active_sellers)
print("Inactive sellers:", inactive_sellers)

print(
    "\nPercentage of active sellers:",
    round(active_sellers / len(sellers) * 100, 2),
    "%"
)

# Overall seller activity
print(
    "\nTotal order items across sellers:",
    seller_analysis["total_order_items"].sum()
)

print(
    "Total product sales across sellers:",
    round(seller_analysis["total_product_sales"].sum(), 2)
)

print(
    "Total freight across sellers:",
    round(seller_analysis["total_freight"].sum(), 2)
)

# Top sellers by order-item count
print("\nTop 15 sellers by order-item count:")

print(
    seller_analysis[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "total_order_items",
            "unique_orders"
        ]
    ]
    .sort_values("total_order_items", ascending=False)
    .head(15)
    .to_string(index=False)
)

# Top sellers by product sales value
print("\nTop 15 sellers by product sales value:")

print(
    seller_analysis[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "total_product_sales",
            "total_order_items"
        ]
    ]
    .sort_values("total_product_sales", ascending=False)
    .head(15)
    .to_string(index=False)
)