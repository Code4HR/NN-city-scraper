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
 }


async def get_body(client, url):
    async with client.get(url) as response:
        return await response.read()


def pull_parcel_info(raw_html):
    parcel = {}
    soap = BeautifulSoup(raw_html, "lxml")
    # Get the Parcel Head Information
    dataheaders = soap.find_all("td", class_=re.compile("DataletHeaderTop"))
    if (dataheaders == []):
        print ("Doesn't Exist Skipping")
        return None
    parcel['parcel_id'] = dataheaders[0].getText().split("PARID:")[1:]
    parcel['address'] = dataheaders[1].getText().strip()

    # check their tax bills
    rows = soap.find(id="Summary of Taxes and Fees Due").find_all('tr')
    print (len(rows))
    # get row
    for tr in rows:
        # get columns across
        # skip the last columns and first header columns
        row = (tr.find_all('td'))
        colCheck = row[0].getText().strip()
        if (colCheck != "Tax Year" and colCheck != "Total:" and colCheck != ""):
            print(row[0].getText(), len(row[0].getText()))
    return parcel


# Checks if there is data on file for this parcel number
def has_data():
    return False

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    for url_offset in range(base_end - base_num):
        raw_html = loop.run_until_complete(get_body(client, base_url.format(base_num + url_offset)))
        parcel = pull_parcel_info(raw_html)
        if parcel:
            print (parcel)
    client.close()
