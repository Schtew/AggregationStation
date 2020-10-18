# https://www.washingtonpost.com/politics/courts_law/supreme-court-census-undocumented-immigrants/2020/10/16/cf8288be-0f51-11eb-8074-0e943a91bf08_story.html
import json
from adjective_polarization import ArticleScrapper
from PolBiasScraper import PolBiasScraper
from retrieve import Retrieve
from datetime import datetime

class main():
    def __init__(self):
        # Instance Varibles
        self.BiasScrap = PolBiasScraper()
        self.ArticleScrap = ArticleScrapper()
        self.Retrie = Retrieve()

    def retrieveData(self, num = 10):
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%Y-%m-%d-%H-%M")

        data = self.Retrie.retrieve(timestamp, num)
        data = data['articles'][:num]
        for article in data:
            article["metrics"].update(self.ArticleScrap.parseURL(article["url"]))
            buildUrlFacts = "https://mediabiasfactcheck.com/" + article["media_name"].lower().replace(" ", "-")
            #print(buildUrlFacts)
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
                        metricscores[x] = 5
                    elif article["metrics"][x] == "Mostly Credible":
                        metricscores[x] = 3.5
                    elif article["metrics"][x] == "Not always Credible or Reliable":
                        metricscores[x] = 2
                    else:
                        metricscores[x] = 0 
            article["metricscores"] = metricscores

        with open("json/data_{0}.json".format(timestamp), "w") as file:
            json.dump(data, file)

        return data
                    # do something else


if __name__ == "__main__":
    m = main()
    m.retrieveData()
