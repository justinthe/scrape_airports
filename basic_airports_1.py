from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://indonesiaairport.com/provinces/index.htm')
bs = BeautifulSoup(html, "html.parser")
# print(bsObj.h1)

titles = bs.findAll("p", {"align": "justify"}, limit=1)
print(titles[0].get_text())
# for title in titles:
#     print(title.get_text())

# airports_by_location_links = bs.findAll("td", {"height": "15", "width": "160", "bordercolor": "#C0C0C0"})
# width: 160 or 227
airports_by_location_links = bs.findAll("td", {"height": "15", "width": re.compile("[12][62][07]"), "bordercolor": "#C0C0C0"})
# for airport_by_location_link in airports_by_location_links:
    # print(airport_by_location_link.get_text())

links = [link.find('a') for link in airports_by_location_links]

base_link = 'http://indonesiaairport.com/provinces/'
filename = "airports_location_links.csv"
f = open(filename, "w+")
for link in links:
    # print(link['href'])
    to_write = base_link + str(link['href']) + "\n"
    # print(to_write)
    f.write(to_write)

f.close()

