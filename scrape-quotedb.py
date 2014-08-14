import urllib2
from lxml import etree
import time

base_url = 'http://www.quotedb.com/quotes/'

def getDataFromPage(pageContents):
    tree = etree.HTML(pageContents)
    result = {}

    quote = tree.xpath("string(//input[@name='text']/@value)")
    author = tree.xpath("string(//font[@class='text'][position()=3]/b/text())")
    category = tree.xpath("string(//font[@class='text'][position()=4]/a/text())")
    result['quote'] = quote
    result['author'] = author
    result['category'] = category

    return result

def getPage(index):
    url = base_url + str(index)
    pageContents = urllib2.urlopen(url).read()
    return pageContents

if __name__ == '__main__':
    for i in range(100, 125):
        page = getPage(i)
        rec = getDataFromPage(page)
        print i, rec['quote'], '==>', rec['author']
        print '\n\n'
        time.sleep(5)
