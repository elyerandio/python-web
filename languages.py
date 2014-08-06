import requests
from bs4 import BeautifulSoup
import codecs

url = 'http://www.101languages.net/chinese/most-common-chinese-words/'

page = requests.get(url)
soup = BeautifulSoup(page.text)

f = codecs.open('chinese.txt', 'w', 'utf-8')

tbl = soup.find('table', attrs={'id' : 'tablepress-13'})
col1 = tbl.find_all('td', attrs={'class' : 'column-1'})
col2 = tbl.find_all('td', attrs={'class' : 'column-2'})
col3 = tbl.find_all('td', attrs={'class' : 'column-3'})

for i in range(len(col1)):
    f.write(col1[i].text)
    f.write("\t")
    f.write(col2[i].text.split('\n')[0].strip())
    f.write("\t")
    f.write(col3[i].text)
    f.write("\n")

f.close()

