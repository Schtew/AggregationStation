import requests 
from bs4 import BeautifulSoup

class PolBiasScraper():
    URL = 'https://mediabiasfactcheck.com/the-australian'
    # results = soup.select('.entry-title')[0]

    def parseURL(URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find("img",{"data-attachment-id": True})["alt"]
    #    print(results.split(" - ")[3])
        for x in results.split(" - "):
            print(x)

    parseURL(URL)