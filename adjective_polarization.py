from newspaper import Article
import glob

class ArticleScrapper():
    url = 'https://www.foxnews.com/us/free-speech-rally-marred-by-violence-as-counterprotesters-storm'

    def check_update():
        filename = None
        path = "json/query_*.json"
        if glob.glob(path) == []:
            print("Existing data file not found...")
        else:
            filename = sorted(glob.glob(path))[len(glob.glob(path))-1]
        return filename

    def parseURL(url):
        article = Article(url)
        article.html
        print(article.authors)
        print(article.text)
        if article.authors != None:
            authors = article.authors


        metrics = {"author": authors}
        print(metrics)

    parseURL(url)