import mechanize
from bs4 import BeautifulSoup
import urllib
import os

def album_extract(soup, year):
    table = soup.find('table', border=1)
    for row in table.findAll('tr')[1:]:
        cols = row.findAll('td')
        rank = cols[0].text
        artist = cols[1].text
        album = cols[2].text
        cover_link = cols[3].img['src']
        record = (str(year), rank, album, artist, cover_link)
        print >> outfile, "|".join(record)

        # download cover picture
        save_as = os.path.join('.', 'album', album + '.jpg')
        urllib.urlretrieve('http://palewire.com' + cover_link, save_as)
        print "Downloaded %s album cover" % album

outfile = open('albums.txt', 'w')
br = mechanize.Browser()
url = 'http://www.palewire.com/scrape/albums/2007.html'
page1 = br.open(url)
html1 = page1.read()
soup1 = BeautifulSoup(html1)
album_extract(soup1, 2007)

page2 = br.follow_link(text="Next")
html2 = page2.read()
soup2 = BeautifulSoup(html2)
album_extract(soup2, 2006)

outfile.close()
