# https://hleecaster.com/python-web-crawling-with-beautifulsoup/

from requests_html import HTMLSession
import requests
import time
from bs4 import BeautifulSoup

s = HTMLSession()
cookies = driver.get_cookies()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ; NCLIENT50_AAP21BE089B46F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }

webpage = requests.get(
        "https://etherscan.io/nfttracker?contractAddress=0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258#trade",
        headers=headers)

time.sleep(60)

soup = BeautifulSoup(webpage.content, "html.parser")
print(soup.select('head > title'))
# print(len(soup.select("#content > section.cards-wrap > article > a > div.card-desc")))
# for s in soup.select("#content > section.cards-wrap > article > a > div.card-desc > h2"):
#     print(s.text)


#content > section.cards-wrap > article:nth-child(2)