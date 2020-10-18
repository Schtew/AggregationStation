# https://www.washingtonpost.com/politics/courts_law/supreme-court-census-undocumented-immigrants/2020/10/16/cf8288be-0f51-11eb-8074-0e943a91bf08_story.html
import json
from adjective_polarization import ArticleScrapper
from PolBiasScraper import PolBiasScraper
from retrieve import Retrieve

class main():
    def __init__(self):
        # Instance Varibles
        self.BiasScrap = PolBiasScraper()
        self.ArticleScrap = ArticleScrapper()
        self.Retrie = Retrieve()

    def retrieveData(self, num = 10):
        data = self.Retrie.retrieve(num)
        data = data['articles'][:num]
        for article in data:
            article["metrics"].update(self.ArticleScrap.parseURL(article["url"]))
            buildUrlFacts = "https://mediabiasfactcheck.com/" + article["media_name"].lower().replace(" ", "-")
            print(buildUrlFacts)
            article["metrics"].update(self.BiasScrap.parseURL(buildUrlFacts))

            # calculations
            metricscores = {}
            for x in article["metrics"]:
                if x == "Bias":
                    if article["metrics"][x] == "Left Center Bias" or article["metrics"][x] == "Right Center Bias":
                        metricscores[x] = 3
                    elif article["metrics"][x] == "Right Bias" or article["metrics"][x] == "Left Bias":
                        metricscores[x] = 1
                    elif article["metrics"][x] == "Least Biased":
                        metricscores[x] = 5
                    # credibilityscores[y] = 1
                    # do something to calculate weight of bias
                if x == "Credibility":
                    if article["metrics"][x] == "Credible":
                        metricscores[x] == 5
                        
                    # do something else

            #article["credibilityscores"] = credibilityscores



        print(data)
        return data

if __name__ == "__main__":
    m = main()
    m.retrieveData()
