from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd


def openUrl(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    return bs


data = pd.read_csv('airports_location_links.csv', header=None)
data.columns = ['url']
links = data['url'].tolist()

for link in links:
    bs = openUrl(link)
    title = bs.find("p", {"align": "justify"})
    # city = re.findall('[Aa]irports in', title.get_text())
    city = title.get_text().replace(" ", "_").lower()
    print(city)



