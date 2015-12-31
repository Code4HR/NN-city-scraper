import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup


base_url = "http://assessment.nnva.gov/PT/Datalets/PrintDatalet.aspx?pin={}&gsp=TAXES_PARENT&taxyear=2016&jur=700&ownseq=0&card=1&roll=REAL&State=1&item=1&items=-1&all=all&ranks=Datalet"
base_num = 100000101
base_end = 100000107


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
 "penalty": "",
 "interest": "",
 "deferred_taxes": "",
 "balance_due": "",
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
