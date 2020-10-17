import requests 
from bs4 import BeautifulSoup

URL = 'https://mediabiasfactcheck.com/fox-news/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
# results = soup.select('.entry-title')[0]
results = soup.find("img",{"data-attachment-id": True})["alt"]

for x in results.split("-"):
    print(x)

print(results)


