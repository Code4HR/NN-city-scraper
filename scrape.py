import aiohttp
import asyncio
import csv
import re
import json

from bs4 import BeautifulSoup
import psycopg2
import sys

with open("parcel-points.json", 'r') as parcel_data:
  parcel_data = json.load(parcel_data)


base_url = "http://assessment.nnva.gov/PT/Datalets/PrintDatalet.aspx?pin={}&gsp=TAXES_PARENT&taxyear=2016&jur=700&ownseq=0&card=1&roll=REAL&State=1&item=1&items=-1&all=all&ranks=Datalet"
# lots populated 312020434

# Parcel model for properties
{"parcel_id": "",
 "address": "",
 "raw_html": "",
 }

# Tax and Fees Due Model
{"tax_year": "",
 "type": "",
 "cycle": "",
 "due_date": "",
 "taxes": "",
 "fees": "",
 "penalty": "",
 "interest": "",
 "deferred_taxes": "",
 "balance_due": "",
 "parcel_id": "",  # our fake foreign keys
 "active": "",  # theres an attribute about if the parcel is active
 }


async def get_body(client, url):
    async with client.get(url) as response:
        return await response.read()

could_not_find = []
taxes_not_owed = []


def pull_parcel_info(raw_html, prop=None):
    parcel = {}
    soap = BeautifulSoup(raw_html, "lxml")
    # Get the Parcel Head Information
    dataheaders = soap.find_all("td", class_=re.compile("DataletHeaderTop"))
    if (dataheaders == []):
        # print ("Doesn't Exist Skipping")
        could_not_find.append(prop)
        return None
    parcel['parcel_id'] = dataheaders[0].getText().split("PARID:")[1:][0].strip()
    parcel['address'] = dataheaders[1].getText().strip()

    # check their tax bills
    owes_taxes = soap.find(id="Summary of Taxes and Fees Due")
    if (owes_taxes is None):
        # print ("No Taxes Owed")
        taxes_not_owed.append(prop)
        return None
    rows = owes_taxes.find_all('tr')
    # print (len(rows))
    # get row
    for tr in rows:
        # get columns across
        # skip the last columns and first header columns
        row = (tr.find_all('td'))
        colCheck = row[0].getText().strip()
        if (colCheck != "Tax Year" and colCheck != "Total:" and colCheck != ""):
            entry = '"'
            entry = '","'.join(str(v.getText()) for v in row)
            data = '"{}","{}","{}","{}"'.format(parcel['parcel_id'], parcel['address'], prop["owner"], entry)
            print(data)
    return parcel


if __name__ == '__main__':

    city_props = []
    # Read in Data
    with open('output.csv') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         city_props.append(row)

    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    for prop in city_props:
        url = base_url.format(prop['parcel_id'])
        raw_html = loop.run_until_complete(get_body(client, url))
        parcel = pull_parcel_info(raw_html, prop=prop)
        # if parcel:
        #     print (parcel)
    client.close()
    print ("Could not find, {} properties", len(could_not_find))
    print ("No Owed Taxes on, {} properties", len(taxes_not_owed))

