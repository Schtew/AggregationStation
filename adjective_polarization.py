import requests
from newspaper import Article
from newspaper import fulltext
import glob
from textblob import TextBlob


class ArticleScrapper():
    url1 = 'https://www.foxnews.com/us/free-speech-rally-marred-by-violence-as-counterprotesters-storm'
    def __init__(self, url=url1):
        self.url = url
    # def check_update():
    #     filename = None
    #     path = "json/query_*.json"
    #     if glob.glob(path) == []:
    #         print("Existing data file not found...")
    #     else:
    #         filename = sorted(glob.glob(path))[len(glob.glob(path))-1]
    #     return filename

    def parseURL(self, url = url1):
        article = Article(url)
        metrics = {}
        articleText = fulltext(requests.get(url).text)
        articleSentiment = TextBlob(articleText).sentiment
        metrics["polarity"] = articleSentiment.polarity

        metrics["subjectivity"] = articleSentiment.subjectivity
        print(metrics)
        return metrics
if __name__ == "__main__":
    a = ArticleScrapper()
    a.parseURL()
    