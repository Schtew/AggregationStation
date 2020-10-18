import requests
from newspaper import Article
from newspaper import fulltext
import glob
from textblob import TextBlob

class ArticleScrapper():
    url = 'https://www.usatoday.com/story/news/politics/2020/10/17/fbi-probes-possible-russia-link-hunter-biden-data-trump-ally-giuliani/3661895001/'

    # def check_update():
    #     filename = None
    #     path = "json/query_*.json"
    #     if glob.glob(path) == []:
    #         print("Existing data file not found...")
    #     else:
    #         filename = sorted(glob.glob(path))[len(glob.glob(path))-1]
    #     return filename

    def parseURL(url):
        article = Article(url)
        metrics = {}
        
        articleText = fulltext(requests.get(url).text)
        articleSentiment = TextBlob(articleText).sentiment
        metrics["polarity"] = articleSentiment.polarity
        metrics["subjectivity"] = articleSentiment.subjectivity
        print(metrics)

    parseURL(url)