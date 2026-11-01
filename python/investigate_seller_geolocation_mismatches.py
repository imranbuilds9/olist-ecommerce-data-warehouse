import csv
from collections import defaultdict

geo_states = defaultdict(set)

with open(
    r"data\raw\olist_geolocation_dataset.csv",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        zip_code = row["geolocation_zip_code_prefix"]
        state = row["geolocation_state"]

        geo_states[zip_code].add(state)


missing = []
mismatches = []

with open(
    r"data\raw\olist_sellers_dataset.csv",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        zip_code = row["seller_zip_code_prefix"]
        seller_state = row["seller_state"]

        available_states = geo_states.get(zip_code, set())

        if not available_states:
            missing.append(row)

        elif seller_state not in available_states:
            mismatches.append({
                "seller_id": row["seller_id"],
                "zip": zip_code,
                "seller_city": row["seller_city"],
                "seller_state": seller_state,
                "geo_states": sorted(available_states)
            })


print("\nMISSING ZIP PREFIX RECORDS:", len(missing))

for row in missing:
    print(
        "Seller:", row["seller_id"],
        "| ZIP:", row["seller_zip_code_prefix"],
        "| City:", row["seller_city"],
        "| State:", row["seller_state"]
    )


print("\nSTATE MISMATCH RECORDS:", len(mismatches))

for row in mismatches:
    print(
        "\nSeller:", row["seller_id"],
        "| ZIP:", row["zip"],
        "| City:", row["seller_city"],
        "| Seller state:", row["seller_state"],
        "| Geolocation states:", row["geo_states"]
    )