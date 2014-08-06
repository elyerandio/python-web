from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

base_url = ("http://www.chicagomag.com/Chicago-Magazine/"
            "November-2012/Best-Sandwiches-Chicago/")

soup = BeautifulSoup(urlopen(base_url).read())
sammies = soup.find_all('div', attrs={'class','sammy'})
sammy_urls = [div.a['href'] for div in sammies]

with open('best-sandwiches.csv', "w") as f:
    fieldnames = ("rank", "sandwich", "restaurant", "description", "price",
                    "address", "phone", "website")
    output = csv.writer(f, delimiter="\t")
    output.writerow(fieldnames)

    for url in sammy_urls:
        url = url.replace("http://www.chicagomag.com","")   # inconsistent URL, delete from start because some URLs have http while others have no http
        page = urlopen("http://www.chicagomag.com{0}".format(url))
        soup = BeautifulSoup(page.read()).find('div', attrs={'class','content post'})
        
