import requests
from bs4 import BeautifulSoup

url = "http://www.yellowpages.com/marling-mo/restaurants"
page = requests.get(url)

soup = BeautifulSoup(page.text)

# get the main content
main = soup.find(id = "main-content")

# get the content info
info = main.find_all(attrs={"class","info"})

i = 1
for item in info:
    print "%d. %s" % (i, item.contents[0].find(attrs={"class","business-name"}).text)
    # get address
    adr = item.contents[1].find(attrs={'class','adr'})
    phone = item.contents[1].find(itemprop='telephone')
    if adr:
        street = adr.find(attrs={'class','street-address'})
        locality = adr.find(attrs={'class','locality'})
        region = adr.find(itemprop='addressRegion')
        zipcode = adr.find(itemprop='postalCode')
        if street or locality or region or zipcode:
            print "\t%s %s %s %s" % (street.text.strip() if street else '',
                    locality.text.strip() if locality else '',
                    region.text.strip() if region else '',
                    zipcode.text.strip() if zipcode else '')
    if phone:
        print "\t%s" % (phone.text.strip())

    i = i + 1
