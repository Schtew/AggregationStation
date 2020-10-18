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
                bias = None
                credibility = None
                l_c = None
                for x in resultsList:
                    if x == "Left Center Bias" or x == "Right Center Bias" or x ==  "Right Bias" or x == "Left Bias" or x == "Least Biased":
                        bias = x
                    elif x == "Credible" or x == "Mostly Credible" or x == "Not always Credible or Reliable" or x == "Not Credible":
                        credibility = x
                    elif x == "Liberal" or x == "Conservative":
                        l_c = x
                return {"Bias": bias, "Credibility": credibility, "Liberal/Conservative": l_c}
            except:
                print("error noises", soup, "\nWith this as the input url: ", url)
        return {}
if __name__ == "__main__":
    p = PolBiasScraper()
    print(p.parseURL())
    a = ArticleScrapper()
    a.parseURL()