import requests 
from bs4 import BeautifulSoup
from adjective_polarization import ArticleScrapper

class PolBiasScraper():
    URL = 'https://mediabiasfactcheck.com/the-australian'
    # results = soup.select('.entry-title')[0]
    def __init__(self, url = URL):
        self.url = url
    def parseURL(self, url = URL):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find("img",{"data-attachment-id": True})["alt"]
    #    print(results.split(" - ")[3])
        for x in results.split(" - "):
            print(x)
if __name__ == "__main__":
    p = PolBiasScraper()
    p.parseURL()
    a = ArticleScrapper()
    a.parseURL()