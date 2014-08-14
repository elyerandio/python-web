import urllib2
import mechanize
from lxml import etree
import time
from Storage import QuoteStorage

base_url = 'http://www.quotedb.com/quotes/'
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Chrome')]

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

def getPageMech(index):
    url = base_url + str(index)
    resp = br.open(url)
    pageContents = resp.get_data()
    return pageContents

if __name__ == '__main__':
    qs = QuoteStorage('quotesdb-com.db')
    #qs.createDb()
    for i in range(51, 100):
        page = getPage(i)
        rec = getDataFromPage(page)
        qs.addQuote(rec['quote'], rec['author'], rec['category'])
        print i, rec['quote'], '==>', rec['author']
        print '\n'
        time.sleep(2)

    print 'Done!'
    qs.close()
