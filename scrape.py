import urlparse
import urllib
from bs4 import BeautifulSoup
import pprint

url = "http://nytimes.com"

urls = [url]        # queue of urls to scrape
visited = [url]     # historic records of urls visited

while len(urls) > 0:
    try:
        htmltext = urllib.urlopen(urls[0]).read()

    except:
        print urls[0]

    soup = BeautifulSoup(htmltext)

    urls.pop(0)

    pprint.pprint([tag['href'] for tag in soup.findAll('a', href=True)])
    #for tag in soup.findAll('a', href=True):


