import json
from adjective_polarization import ArticleScrapper
from PolBiasScraper import PolBiasScraper
from retrieve import Retrieve
from datetime import datetime


class main():
    def __init__(self):
        self.BiasScrap = PolBiasScraper()
        self.ArticleScrap = ArticleScrapper()
        self.Retrie = Retrieve()
        self.dateTimeObj = datetime.now()
        self.timestamp = self.dateTimeObj.strftime("%Y-%m-%d-%H-%M")
        self.datasetSize = 20
        self.rankedsetSize = 10
        self.maxtags = 30
        self.politicweight = 0.95
        self.maxageseconds = 604800

        self.weight = {
            "age": 0.12,
            "tags": 0.24,
            "polarity": 0.21,
            "subjectivity": 0.13,
            "credibility": 0.13,
            "bias": 0.17
        }

    def percentage(self, article):
        unweighted = {
            "age": 0,
            "tags": 0,
            "polarity": 0,
            "subjectivity": 0,
            "credibility": 0,
            "bias": 0
        }

        # age
        x = (article["metricscores"]["age"] / self.maxageseconds)
        unweighted["age"] = (x + 1) ** (-5 * x)

        # tags
        if article["metricscores"]["tags"] > 1:
            unweighted["tags"] = self.politicweight + ((article["metricscores"]["tags"] - 1) * (1 - self.politicweight))
        else:
            unweighted["tags"] = (article["metricscores"]["tags"]) * (1 - self.politicweight)

        # polarity
        x = abs(article["metricscores"]["polarity"])
        unweighted["polarity"] = x

        # subjectivity
        unweighted["subjectivity"] = article["metricscores"]["polarity"]

        # credibility
        unweighted["credibility"] = article["metricscores"]["credibility"] / 10

        # bias
        unweighted["bias"] = article["metricscores"]["bias"] / 5

        return unweighted

    def mediaBias(self, article):
        article["metrics"].update(self.ArticleScrap.parseURL(article["url"]))
        buildUrlFacts = "https://mediabiasfactcheck.com/" + article["media_name"].lower().replace(" ", "-")
        article["metrics"].update(self.BiasScrap.parseURL(buildUrlFacts))

    def tagQuantification(self, article):
        metricscores = {}
        for x in article["metrics"]:
            if x == "tags":
                metricscores[x] = 0
                if "politics and government" in article["metrics"]["tags"]:
                    metricscores[x] += 1
                if len(article["metrics"]["tags"]) < 31:
                    metricscores[x] += len(article["metrics"]["tags"]) / 30
                else:
                    metricscores[x] += 1
            else:
                metricscores[x] = article["metrics"][x]
        return metricscores

    def retrieveData(self):
        data = self.Retrie.retrieve(self.timestamp, storylimit=self.datasetSize)
        data = data['articles'][:self.datasetSize]

        unrankeddata = {}

        for index, article in enumerate(data):
            print(index+1)

            self.mediaBias(article)

            article["metricscores"] = self.tagQuantification(article)

            # weights
            unweighted = self.percentage(article)

            score = 0
            for metric in unweighted:
                score += unweighted[metric] * self.weight[metric]

            article["score"] = abs(score)
            unrankeddata[abs(score)] = article

        rankeddata = {}

        for index, article in enumerate(sorted(unrankeddata.keys(), reverse=True)):
            rankeddata[index+1] = unrankeddata[article]
            if index == self.rankedsetSize:
                break
        with open("json/data_{0}.json".format(self.timestamp), "w") as file:
            json.dump(rankeddata, file)

        return rankeddata

if __name__ == "__main__":
    m = main()
    m.retrieveData()
