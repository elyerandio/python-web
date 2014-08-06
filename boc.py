import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.chicagoreader.com"

def get_category_links(section_url):
    page = requests.get(section_url)
    soup = BeautifulSoup(page.text)

    boccat = soup.find('dl', attrs={'class','boccat'})
    category_links = [BASE_URL + dd.a['href'] for dd in boccat.find_all('dd') ]
    return category_links

def get_category_winners(category_links):
    winners = {}
    for link in category_links:
        page = requests.get(link)
        soup = BeautifulSoup(page.text)

        # get the category name
        cat = soup.find('div', attrs={'class','storyHead'})
        cat_text = unicode(cat.h1.string.strip())

        # get the winner
        winner = soup.find('h2', attrs={'class','boc1'})
        if winner.a:
            winner_text = unicode(winner.a.string.strip())
        else:
            winner_text = unicode(winner.string.strip())

        # save winner
        print "%s ==> %s" % (cat_text.encode('utf-8','replace'), winner_text.encode('utf-8','replace'))
        winners[cat_text] = winner_text

    
    return winners


section = "http://www.chicagoreader.com/chicago/best-of-chicago-2011-food-drink/BestOf?oid=4106228"
categories = get_category_links(section)
winners = get_category_winners(categories)

for winner in winners:
    print "%s ==> %s" % (winner, winners[winner]);
