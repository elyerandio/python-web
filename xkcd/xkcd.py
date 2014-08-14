import urllib
import re

class Downloader():
    '''
    Class to retrieve HTML code
    and binary files from a specific website
    '''
    def __init__(self, url):
        self.url = self.contents = ''
        self.contents = ''

    def download(self, image_name='', is_image=False):
        browser = urllib.urlopen(self.url)
        response = browser.getcode()
        if response == 200:
            self.contents = browser.read()

        if is_image:
            image_file = open(image_name, "wb")
            image_file.write(self.contents)
            image_file.close()

class xkcdParser(Downloader):
    '''
    Class for parsing xkcd.com
    '''
    def get_last_comic_nr(self):
        try:
            last_comic_nr = re.search(r"Permanent link to this comic: http://xkcd.com/(\d+)", self.contents).group(1)
            last_comic_nr = int(last_comic_nr)
        except:
            last_comic_nr = None
