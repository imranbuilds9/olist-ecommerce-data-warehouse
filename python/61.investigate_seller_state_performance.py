import pandas as pd

sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")
items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

# Aggregate activity for each seller
seller_activity = (
    items.groupby("seller_id")
    .agg(
        total_items=("order_id", "count"),
        unique_orders=("order_id", "nunique"),
        product_sales=("price", "sum"),
        freight_value=("freight_value", "sum")
    )
    .reset_index()
)

# Attach seller state
seller_data = sellers.merge(
    seller_activity,
    on="seller_id",
    how="left"
)

# Aggregate by state
state_performance = (
    seller_data.groupby("seller_state")
    .agg(
        seller_count=("seller_id", "nunique"),
        total_items=("total_items", "sum"),
        unique_seller_orders=("unique_orders", "sum"),
        product_sales=("product_sales", "sum"),
        freight_value=("freight_value", "sum")
    )
    .reset_index()
)

# Calculate contribution percentages
total_sales = state_performance["product_sales"].sum()

state_performance["sales_share_pct"] = (
    state_performance["product_sales"] / total_sales * 100
)

state_performance["seller_share_pct"] = (
    state_performance["seller_count"] / len(sellers) * 100
)

# Average product sales per seller
state_performance["sales_per_seller"] = (
    state_performance["product_sales"] /
    state_performance["seller_count"]
)

state_performance = state_performance.sort_values(
    "product_sales",
    ascending=False
)

print("========== SELLER STATE PERFORMANCE ==========")

print("\nState-level performance:")
print(
    state_performance.round(2).to_string(index=False)
)

print("\nTop 5 states by product sales:")
print(
    state_performance[
        ["seller_state", "seller_count", "product_sales", "sales_share_pct"]
    ].head(5).round(2).to_string(index=False)
)

print("\nTop 5 states by seller count:")
print(
    state_performance.sort_values(
        "seller_count",
        ascending=False
    )[
        ["seller_state", "seller_count", "product_sales", "sales_share_pct"]
    ].head(5).round(2).to_string(index=False)
)

print("\nReconciliation:")
print("Total sellers:", state_performance["seller_count"].sum())
print("Original sellers:", len(sellers))

print("Total order items:", state_performance["total_items"].sum())
print("Original order items:", len(items))

print("Total product sales:", round(total_sales, 2))
print("Original product sales:", round(items["price"].sum(), 2))