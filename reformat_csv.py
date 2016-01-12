""" Reformats the list we have of Newport News Addresses to the Parcel-points and plucks the parcel ID

if "@@@@@" for parcel_id the look up was not successful for the property """

import csv
import json

with open("parcel-points.json", 'r') as parcel_data:
  parcel_data = json.load(parcel_data)

to_save = []
with open('test.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
     print(row["street_num"] + " " + row["street"])
     for parcel in iter(parcel_data["features"]):
        addr = parcel["properties"]
        query = row["street_num"] + " " + row["street"]
        street = "{} {}".format(addr["HouseNo"], addr["Street"])
        if query in street:
            # print("found ", parcel)
            item = {"street_num": row["street_num"], "street": row["street"], "owner": row["owner"], "parcel_id": addr["REISID"]}
            to_save.append(item)
            continue

with open('formatted.csv', 'w') as csvfile:
    fieldnames = ["street_num", "street", "owner", "parcel_id"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in to_save:
       writer.writerow({"street_num": row["street_num"], "street": row["street"], "owner": row["owner"], "parcel_id": addr["REISID"]})


