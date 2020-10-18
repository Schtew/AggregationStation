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

    def retrieveData(self, num = 90):
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%Y-%m-%d-%H-%M")

        data = self.Retrie.retrieve(timestamp, num)
        data = data['articles'][:num]
        unrankeddata = {}
        count = 1
        for article in data:
            print(count)
            count += 1
            article["metrics"].update(self.ArticleScrap.parseURL(article["url"]))
            buildUrlFacts = "https://mediabiasfactcheck.com/" + article["media_name"].lower().replace(" ", "-")
            #print(buildUrlFacts)
            article["metrics"].update(self.BiasScrap.parseURL(buildUrlFacts))

            # calculations
            metricscores = {}
            for x in article["metrics"]:
                if x == "bias":
                    if article["metrics"][x] == "Left Center Bias" or article["metrics"][x] == "Right Center Bias":
                        metricscores[x] = 3
                    elif article["metrics"][x] == "Right Bias" or article["metrics"][x] == "Left Bias":
                        metricscores[x] = 1
                    elif article["metrics"][x] == "Least Biased":
                        metricscores[x] = 5
                    else:
                        metricscores[x] = 0
                elif x == "credibility":
                    credibilityDict = {"Credible": 10, "Mostly Credible": 7, "Not always Credible or Reliable": 4}
                    if article["metrics"][x] in credibilityDict:
                        metricscores[x] = credibilityDict[article["metrics"][x]]
                    else:
                        metricscores[x] = 0
                elif x == "tags":
                    metricscores[x] = 0
                    if "politics and government" in article["metrics"]["tags"]:
                        metricscores[x] += 1
                    if len(article["metrics"]["tags"]) < 31:
                        metricscores[x] += len(article["metrics"]["tags"]) / 30
                    else:
                        metricscores[x] += 1
                else:
                    metricscores[x] = article["metrics"][x]

            article["metricscores"] = metricscores

            # weights
            unweighted = {
                "age": 0,
                "tags": 0,
                "polarity": 0,
                "subjectivity": 0,
                "credibility": 0,
                "bias": 0
            }

            # age
            x = (article["metricscores"]["age"] / 604800)
            unweighted["age"] = (x + 1) ** (-5*x)

            # tags
            politicweight = 0.9
            if article["metricscores"]["tags"] > 1:
                unweighted["tags"] = politicweight + ((article["metricscores"]["tags"] - 1) * (1-politicweight))
            else:
                unweighted["tags"] = (article["metricscores"]["tags"]) * (1-politicweight)

            # polarity
            x = abs(article["metricscores"]["polarity"])
            unweighted["polarity"] = x

            #subjectivity
            unweighted["subjectivity"] = article["metricscores"]["polarity"]

            #credibility
            unweighted["credibility"] = article["metricscores"]["credibility"] / 10

            #bias
            unweighted["bias"] = article["metricscores"]["bias"] / 5

            weight = {
                "age": 0.09,
                "tags": 0.21,
                "polarity": 0.17,
                "subjectivity": 0.11,
                "credibility": 0.25,
                "bias": 0.17
            } # needs to add up to 1

            score = 0
            for metric in unweighted:
                score += unweighted[metric] * weight[metric]

            article["score"] = abs(score)
            unrankeddata[abs(score)] = article

            #print("{0} , {1}".format(article["url"], article["score"]))



        rankeddata = {}
        rank = 1
        for article in sorted(unrankeddata.keys(), reverse=True):
            rankeddata[rank] = unrankeddata[article]
            rank += 1
            if rank == 55:
                break;
            #print("{0} , {1}".format(unrankeddata[article]["url"], unrankeddata[article]["score"]))

        with open("json/data_{0}.json".format(timestamp), "w") as file:
            json.dump(rankeddata, file)

        return rankeddata

if __name__ == "__main__":
    m = main()
    m.retrieveData()
