import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup


base_url = "http://assessment.nnva.gov/PT/datalets/datalet.aspx?mode=taxes_parent&UseSearch=no&pin={}&jur=700&taxyr=2016&LMparent=20"
base_num = 100000102
base_end = 100000103

print(base_url.format(base_num))

async def get_body(client, url):
    async with client.get(url) as response:
        return await response.read()


def pull_parcel_info(raw_html):
    parcel = {}
    soap = BeautifulSoup(raw_html, "lxml")
    # Get the Parcel Head Information
    dataheaders = soap.find_all("td", class_=re.compile("DataletHeaderTop"))
    parcel['parcel_id'] = dataheaders[0].getText().split("PARID:")[1:]
    parcel['address'] = dataheaders[1].getText()
    print(parcel)
    return True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    for url_offset in range(base_end - base_num):
        raw_html = loop.run_until_complete(get_body(client, base_url.format(base_num + url_offset)))
        pull_parcel_info(raw_html)
    client.close()
