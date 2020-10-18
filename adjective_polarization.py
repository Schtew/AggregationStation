from newspaper import Article
import glob

class ArticleScrapper():
    url = 'https://www.usatoday.com/story/news/politics/2020/10/17/fbi-probes-possible-russia-link-hunter-biden-data-trump-ally-giuliani/3661895001/'

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

        print(article.authors)
        print(article.text)
        if article.authors != None:
            authors = article.authors


        metrics = {"author": authors}
        print(metrics)

    parseURL(url)