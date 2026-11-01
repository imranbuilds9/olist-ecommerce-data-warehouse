import csv
from collections import Counter

path = r"data\raw\olist_geolocation_dataset.csv"

total = 0
outside_brazil = 0

outside_by_state = Counter()
outside_by_reason = Counter()

samples = []

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total += 1

        lat = float(row["geolocation_lat"])
        lng = float(row["geolocation_lng"])

        state = row["geolocation_state"]
        city = row["geolocation_city"]
        zip_code = row["geolocation_zip_code_prefix"]

        reasons = []

        if lat < -35 or lat > 6:
            reasons.append("latitude_outside")

        if lng < -74 or lng > -32:
            reasons.append("longitude_outside")

        if reasons:
            outside_brazil += 1
            outside_by_state[state] += 1

            for reason in reasons:
                outside_by_reason[reason] += 1

            if len(samples) < 20:
                samples.append({
                    "zip": zip_code,
                    "lat": lat,
                    "lng": lng,
                    "city": city,
                    "state": state,
                    "reasons": reasons
                })


print("\nTOTAL ROWS:", total)
print("Rows outside screening boundaries:", outside_brazil)

print("\n--- OUTLIERS BY STATE ---")

for state, count in outside_by_state.most_common():
    print(state, ":", count)

print("\n--- OUTLIER REASONS ---")

for reason, count in outside_by_reason.items():
    print(reason, ":", count)

print("\n--- FIRST 20 OUTLIER RECORDS ---")

for item in samples:
    print(
        "\nZIP:", item["zip"],
        "| Latitude:", item["lat"],
        "| Longitude:", item["lng"],
        "| City:", item["city"],
        "| State:", item["state"],
        "| Reasons:", item["reasons"]
    )