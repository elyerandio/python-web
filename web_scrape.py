import requests
import bs4

root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'

def get_video_page_urls():
    page = requests.get(index_url)
    soup = bs4.BeautifulSoup(page.text)
    return [a.attrs.get('href') for a in soup.select('div.video-summary-data a[href^=/video]')]

links = get_video_page_urls()
for link in links:
    print link
