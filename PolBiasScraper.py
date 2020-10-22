import requests
from bs4 import BeautifulSoup
from adjective_polarization import ArticleScrapper


class PolBiasScraper():
    def parseURL(self, url='https://mediabiasfactcheck.com/the-australian'):
        polmetrics = {"bias": 0, "credibility": 0, "liberal/conservative": 0}
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                results = soup.find("img", {"data-attachment-id": True})["alt"].split(" - ")
                for x in results:
                    bias_dict = {"Left Center Bias": 3, "Right Center Bias": 3, "Right Bias": 1, "Left Bias": 1,
                                "Least Biased": 5}
                    credibility_dict = {"Credible": 10, "Mostly Credible": 7, "Not always Credible or Reliable": 4,
                                       "Not Credible": 0}
                    l_c_dict = {"Liberal": 1, "Conservation": 0}
                    if x in bias_dict.keys():
                        polmetrics["bias"] = bias_dict[x]
                    elif x in credibility_dict.keys():
                        polmetrics["credibility"] = credibility_dict[x]
                    elif x in l_c_dict:
                        polmetrics["l_c"] = l_c_dict[x]
                return polmetrics
            except:
                print("Unable to collect PolBias data for url {0}".format(url))
        return polmetrics


if __name__ == "__main__":
    p = PolBiasScraper()
    print(p.parseURL())
    a = ArticleScrapper()
    a.parseURL()
