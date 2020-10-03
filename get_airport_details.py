from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


def openUrl(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    return bs

# get all links in folder and loop over all links
base_folder = "scrape_data/"

for file_name in os.listdir(base_folder):
    afile = base_folder + file_name
    data = pd.read_csv(afile)
    links = data['url'].tolist()
    airports = data['AirportName'].tolist()
    airports_df = pd.DataFrame(list(zip(links, airports)), columns = ['url', 'airport_name'])
    # print(airports_df.head())
    # 1. open link
    # 2. use AirportName as filename
    # 3. read data from opened link
    # 4. write data to #2
