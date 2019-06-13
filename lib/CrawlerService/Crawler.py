from urllib.request import urlopen
from requests import Request
from bs4 import BeautifulSoup as soup


class Crawler():
    # TODO: to be tested

    current_url = None
    browser_header = {'User-Agent': "Mozilla/5.0 (X11; Linux i686; rv:64.0) \
                      Gecko/20100101 Firefox/64.0"}

    def __init__(self, url):
        self.current_url = url

    def parse_HTML(self) -> "page_soup":
        # html parsing
        client = urlopen(Request(
            self.current_url, headers=self.browser_header))
        page_html = client.read()
        client.close()
        page_soup = soup(page_html, 'html.parser')
        return page_soup
