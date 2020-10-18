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
                    biasDict = ["Left Center Bias", "Right Center Bias", "Right Bias", "Left Bias", "Least Biased"]
                    credibilityDict = ["Credible", "Mostly Credible", "Not always Credible or Reliable", "Not Credible"]
                    l_c_Dict = ["Liberal", "Conservation"]
                    if x in biasDict:
                        bias = x
                    elif x in credibilityDict:
                        credibility = x
                    elif x in l_c_Dict:
                        l_c = x
                return {"bias": bias, "credibility": credibility, "liberal/conservative": l_c}
            except:
                abc = 1
                #print("error noises", soup, "\nWith this as the input url: ", url)
        return {"bias": None, "credibility": None, "liberal/conservative": None}
if __name__ == "__main__":
    p = PolBiasScraper()
    print(p.parseURL())
    a = ArticleScrapper()
    a.parseURL()