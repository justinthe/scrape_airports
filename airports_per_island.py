from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import unicodedata

def openUrl(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    return bs

data = pd.read_csv('airports_location_links.csv', header=None)
data.columns = ['url']
links = data['url'].tolist()

base_url = "http://indonesiaairport.com/"

for link in links:
    bs = openUrl(link)
    title = bs.find("p", {"align": "justify"})
    # island = title.get_text().replace(" ", "_").lower()
    island = title.get_text()
    island =  ''.join(e for e in island if e.isalnum()) 
    # print(island)
    
    base_folder = "scrape_data/"
    filename = base_folder + island + ".csv"
    f = open(filename, "w+")

    table = bs.find("table", {"id": "AutoNumber4"})
    rows = table.find_all("td")
    urls = table.find_all("a")
    
    # to check the list
    # i = 0
    templist = []
    a_row = ""
    
    # add column header manually 
    templist.append("url,")
    
    # sometimes relative url move back to its grandparent folder
    pattern = "../../"

    # for row in rows:
    for i, row in enumerate(rows):
        to_write = row.get_text()
        to_write = re.sub('[^A-Za-z0-9\s]+', '', to_write) 
        # print("{}: {}".format(i, to_write))
        # i = i + 1
        to_write = ''.join(e for e in to_write if e.isalnum()) + ","
        
        # Airport Name, ICAO, IATA, city served
        # every 4 items, add new line
        if (i+1) % 4 == 0:
            to_write = to_write + "\n"
        
        # url
        r_url = row.find("a")
        # print("Index: {}, Row: {}".format(i, to_write))

        if i % 4 == 0 and i != 0: 

            if r_url is not None:
                # print(r_url)
                str_url = str(r_url["href"])
                if re.search(pattern, str_url):
                    str_url = str_url.replace(pattern, "")
                else:
                    base_url = link.replace("index.htm", "")

                str_url = base_url + str_url + ","
                templist.append(str_url)
            else:
                templist.append(",")
        
        templist.append(to_write)
        
    

    for i, item in enumerate(templist):
        # print(item)
        f.write(item)

        # all these aren't needed, all done in main loop
        # use repr(item) to show if string is surrounded with special characters
        # print("{}: {}".format(i, repr(item)))
        # it is - strip them down
        # print("{}: {}".format(i, (''.join(e for e in item if e.isalnum()))))

        # item = ''.join(e for e in item if e.isalnum())
        # a_row = a_row + item + ","

        # Airport Name, ICAO, IATA, city served
        # every 4 items, add new line
        # if (i+1) % 5 == 0:
        #     a_row = a_row + "\n"
            # print("\n")
        
        
    # print(a_row)
    # f.write(a_row)
    f.close()

    # Not being used anymore. include url in main loop
    # # get urls
    # for url in urls:
    #     str_url = str(url['href'])
    #     # original_url = str_url
    #     pattern = "../../"
    #     if re.search(pattern, str_url):
    #         str_url = str_url.replace(pattern, "")
    #     else:
    #         base_url = link.replace("index.htm", "")
            
    #     str_url = base_url +  str_url 
    #     # print("From: {}, to: {}".format(original_url, str_url))


