from urllib.request import urlopen
from requests import Request
from bs4 import BeautifulSoup as soup
import time


class Crawler():
    # TODO: to be tested
    """
    Crawler is intended to be instantiated once per domain. It supports 
    mechanism that make sure it crawl politely.
    """
    browser_header = {'User-Agent': "Mozilla/5.0 (X11; Linux i686; rv:64.0) \
                      Gecko/20100101 Firefox/64.0"}
    current_url = None
    start_time = 0
    crawler_freeze_seconds = None

    def set_crawler(self, url: str, crawler_freeze_seconds: int):
        """
        Register an internal timer when a crawl_website is called.
        """
        if self.is_locked():
            raise Exception('This crawler is locked')

        self.start_time = int(round(time.time() * 1000))
        self.current_url = url
        self.crawler_freeze_seconds = crawler_freeze_seconds

    def crawl_website(self) -> "page_soup":
        """
        Parsing url html to a bs4 soup object.
        """
        if self.is_locked():
            raise Exception('This crawler is locked')

        client = urlopen(Request(
            self.current_url, headers=self.browser_header))
        page_html = client.read()
        client.close()
        page_soup = soup(page_html, 'html.parser')

        self._register_as_used()
        return page_soup

    def is_locked(self) -> bool:
        """
        Check whether the current time is n seconds after starting time.
        """
        unlockable_time = self.start_time + \
            (self.crawler_freeze_seconds * 1000)
        now = int(round(time.time() * 1000))
        if now < unlockable_time or self.current_url != None:
            return True
        else:
            return False

    def _register_as_used(self):
        self.current_url = True
