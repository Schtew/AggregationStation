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
        print(data)
        return data

if __name__ == "__main__":
    m = main()
    m.retrieveData()
