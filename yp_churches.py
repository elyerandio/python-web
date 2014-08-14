import requests
from bs4 import BeautifulSoup
import xlwt

domain = "http://www.yellowpages.com"
href = "/green-acres-fl/churches-places-of-worship?g=green%20acres%2C%20fl&q=churches%20places%20of%20worship&s=relevance"

wb = xlwt.Workbook()
ws = wb.add_sheet('Churches Data')

# write the Header Column
ws.write(0, 0, 'Church Name')
ws.write(0, 1, 'Address')
ws.write(0, 2, 'City')
ws.write(0, 3, 'Zip Code')
ws.write(0, 4, 'State')
ws.write(0, 5, 'Area Code and Phone Number')

row = 1
while True:
    html = requests.get(domain + href)

    soup = BeautifulSoup(html.text)
    page = soup.find(class_ = 'pagination')
    current_page = page.find(class_ = 'disabled').parent

    # get the main content
    main = soup.find(id = "main-content")

    # get the content info
    info = main.find_all(attrs={"class", "info"})

    for item in info:
        index = item.find(attrs={'class': 'index'})
        name = item.find(attrs={'class': 'business-name'})
        print "\n-------------------------\n%s.) %s" % (index.string, name.string)

        ws.write(row, 0, name.string)

        # get address
        adr = item.contents[1].find(attrs={'class', 'adr'})
        phone = item.contents[1].find(itemprop='telephone')
        if adr:
            street = adr.find(attrs={'class', 'street-address'})
            locality = adr.find(attrs={'class', 'locality'})
            state = adr.find(itemprop='addressRegion')
            zipcode = adr.find(itemprop='postalCode')

            if street:
                ws.write(row, 1, street.string)
            if locality:
                city = locality.string.strip()                              # remove trailing spaces
                city = city.strip(',')                                      # remove comma
                ws.write(row, 2, city)
            if zipcode:
                ws.write(row, 3, zipcode.string)
            if state:
                ws.write(row, 4, state.string)

        if phone:
            ws.write(row, 5, phone.string)

        row += 1

    # get next page
    next_page = current_page.nextSibling
    if(next_page):
        href = next_page.a['href']
    else:                                           # last page
        break;


# save Excel file and exit
wb.save('churches.xls')

