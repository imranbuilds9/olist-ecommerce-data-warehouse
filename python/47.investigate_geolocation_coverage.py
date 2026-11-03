import csv

geo_zip_codes = set()
geo_zip_state = set()

with open(
    r"data\raw\olist_geolocation_dataset.csv",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        zip_code = row["geolocation_zip_code_prefix"]
        state = row["geolocation_state"]

        geo_zip_codes.add(zip_code)
        geo_zip_state.add((zip_code, state))


def investigate_file(path, zip_column, state_column, label):

    total = 0
    missing_zip = 0
    mismatched_state = 0

    unique_zip_codes = set()
    unique_zip_state_pairs = set()

    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += 1

            zip_code = row[zip_column]
            state = row[state_column]

            unique_zip_codes.add(zip_code)
            unique_zip_state_pairs.add((zip_code, state))

            if zip_code not in geo_zip_codes:
                missing_zip += 1

            elif (zip_code, state) not in geo_zip_state:
                mismatched_state += 1

    print("\n" + "=" * 55)
    print(label)

    print("TOTAL RECORDS:", total)
    print("UNIQUE ZIP PREFIXES:", len(unique_zip_codes))
    print("UNIQUE ZIP-STATE PAIRS:", len(unique_zip_state_pairs))

    print("RECORDS WITH ZIP NOT FOUND:", missing_zip)
    print("RECORDS WITH ZIP-STATE MISMATCH:", mismatched_state)


investigate_file(
    r"data\raw\olist_customers_dataset.csv",
    "customer_zip_code_prefix",
    "customer_state",
    "CUSTOMERS"
)

investigate_file(
    r"data\raw\olist_sellers_dataset.csv",
    "seller_zip_code_prefix",
    "seller_state",
    "SELLERS"
)