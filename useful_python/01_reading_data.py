import csv
import json

with open("01_reading_data.json") as fp:
    data = json.load(fp)
    print(data.keys())
    print(data["features"][0]["properties"]["LibraryName"])
    headers = data["features"][0]["properties"].keys()
    print(headers)

    with open("01_reading_data.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for datum in data["features"]:
            writer.writerow(datum["properties"])