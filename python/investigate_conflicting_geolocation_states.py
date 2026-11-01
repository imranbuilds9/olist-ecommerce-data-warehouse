import csv
from collections import defaultdict, Counter

path = r"data\raw\olist_geolocation_dataset.csv"

conflicting_zips = {
    "02116", "04011", "21550", "23056",
    "72915", "78557", "79750", "80630"
}

records = defaultdict(list)

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        zip_code = row["geolocation_zip_code_prefix"]

        if zip_code in conflicting_zips:
            records[zip_code].append({
                "state": row["geolocation_state"],
                "city": row["geolocation_city"],
                "lat": float(row["geolocation_lat"]),
                "lng": float(row["geolocation_lng"])
            })


for zip_code in sorted(conflicting_zips):

    print("\n" + "=" * 60)
    print("ZIP PREFIX:", zip_code)

    state_counts = Counter(
        record["state"] for record in records[zip_code]
    )

    print("TOTAL RECORDS:", len(records[zip_code]))

    print("\nSTATE COUNTS:")

    for state, count in state_counts.most_common():
        print(state, ":", count)

    print("\nCITY COUNTS BY STATE:")

    for state in sorted(state_counts):
        city_counts = Counter(
            record["city"]
            for record in records[zip_code]
            if record["state"] == state
        )

        print("\nState:", state)

        for city, count in city_counts.most_common():
            print(" ", city, ":", count)

    print("\nCOORDINATE RANGES BY STATE:")

    for state in sorted(state_counts):
        state_records = [
            record for record in records[zip_code]
            if record["state"] == state
        ]

        latitudes = [r["lat"] for r in state_records]
        longitudes = [r["lng"] for r in state_records]

        print(
            state,
            "| Latitude:", min(latitudes), "to", max(latitudes),
            "| Longitude:", min(longitudes), "to", max(longitudes)
        )