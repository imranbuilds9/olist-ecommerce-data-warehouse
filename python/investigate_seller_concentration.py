import pandas as pd

sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")
items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

# Aggregate seller-level performance
seller_sales = (
    items.groupby("seller_id")
    .agg(
        total_items=("order_id", "count"),
        unique_orders=("order_id", "nunique"),
        product_sales=("price", "sum")
    )
    .reset_index()
)

# Sort sellers by product sales
seller_sales = seller_sales.sort_values(
    "product_sales",
    ascending=False
).reset_index(drop=True)

total_revenue = seller_sales["product_sales"].sum()
total_items = seller_sales["total_items"].sum()

# Calculate cumulative revenue contribution
seller_sales["revenue_share_pct"] = (
    seller_sales["product_sales"] / total_revenue * 100
)

seller_sales["cumulative_revenue_share_pct"] = (
    seller_sales["revenue_share_pct"].cumsum()
)

print("========== SELLER SALES CONCENTRATION ==========")

print("\nTotal sellers:", len(sellers))
print("Sellers with sales:", len(seller_sales))
print("Total product sales:", round(total_revenue, 2))

# Top seller groups
for count in [5, 10, 20, 50, 100]:
    top_revenue = seller_sales.head(count)["product_sales"].sum()
    contribution = top_revenue / total_revenue * 100

    print(
        f"\nTop {count} sellers:"
        f"\nProduct sales: R${top_revenue:,.2f}"
        f"\nRevenue contribution: {contribution:.2f}%"
    )

# Seller revenue distribution
print("\nSeller product sales distribution:")
print(
    seller_sales["product_sales"].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )
)

# Top 10 sellers
print("\nTop 10 sellers by cumulative revenue contribution:")

print(
    seller_sales[
        [
            "seller_id",
            "product_sales",
            "revenue_share_pct",
            "cumulative_revenue_share_pct"
        ]
    ].head(10).to_string(index=False)
)

# Reconciliation
print("\n========== RECONCILIATION ==========")
print("Seller item count:", total_items)
print("Source item count:", len(items))
print("Item count matches:", total_items == len(items))