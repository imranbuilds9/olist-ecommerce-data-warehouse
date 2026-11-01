import pandas as pd

file_path = "data/raw/olist_sellers_dataset.csv"

df = pd.read_csv(file_path)

print("========== SELLER DATASET PROFILE ==========")

print("\nTotal rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique seller IDs:", df["seller_id"].nunique())

print(
    "Duplicate seller IDs:",
    df["seller_id"].duplicated().sum()
)

print("\nUnique ZIP code prefixes:", df["seller_zip_code_prefix"].nunique())

print("\nUnique cities:", df["seller_city"].nunique())

print("\nUnique states:", df["seller_state"].nunique())

print("\nState distribution:")
print(df["seller_state"].value_counts())

print("\nTop 15 cities by seller count:")
print(df["seller_city"].value_counts().head(15))

print("\nSeller ZIP code prefix frequency:")
print(df["seller_zip_code_prefix"].value_counts().head(15))

print("\nSeller records with whitespace-only city names:")
whitespace_cities = df[
    df["seller_city"].astype(str).str.strip().eq("")
]

print(len(whitespace_cities))