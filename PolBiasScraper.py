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
        if(page.status_code == 200):
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                results = soup.find("img",{"data-attachment-id": True})["alt"]
                # print(results.split(" - ")[3])
                resultsList = results.split(" - ")
                for x in resultsList:
                    print(x)
                if len(resultsList) > 3:
                    return {"Bias": resultsList[1], "Crediblity": resultsList[2], "lib/conserv": resultsList[3]}
            except:
                print("error noises", soup, "\nWith this as the input url: ", url)
        return {}
if __name__ == "__main__":
    p = PolBiasScraper()
    print(p.parseURL())
    a = ArticleScrapper()
    a.parseURL()