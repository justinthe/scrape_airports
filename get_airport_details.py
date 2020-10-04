from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


def openUrl(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, "html.parser")
    except HTTPError:
        print("No page found. URL was: {}".format(url))
    return bs

def extractContentAndSave(bs, filename):
    table = bs.find("table", {"id": "AutoNumber3"})
    # content = ''.join(e for e in table.get_text() if e.isalnum())
    raw_content = table.get_text()
    # split text and rejoin them to get rid of special characters. 
    text = raw_content.split()
    content = ""

    fname = "airports_data/" + filename + ".csv"
    # fname = filename + ".csv"
    f = open(fname, "w+")

    for str_text in text:
        content = content + str_text + ' '
    f.write(content)
    # print(content)      
    # f.close()  


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
    
    nan_pattern = "^(?!nan)"
    # nan_pattern = "(bawean)"
    for index, airport_data in airports_df.iterrows():
        if re.search(nan_pattern, str(airport_data[0])):
            url = airport_data[0]
            airport = airport_data[1]
            # print("url: {}; filename: {}".format(airport_data[0], airport_data[1]))
            # print("url: {}; filename: {}".format(url, airport))
            bs = openUrl(url)
            extractContentAndSave(bs, airport)
