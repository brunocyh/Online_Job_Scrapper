import requests
from bs4 import BeautifulSoup
import time

from abc import ABC, abstractmethod

class Crawler:
    """
    Crawler is intended to be instantiated once per domain. It supports 
    mechanism that make sure it crawl politely.
    """
    _browser_header = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    _current_url = None
    _start_time = 0
    _crawler_freeze_seconds = 0

    def configure_crawler(self, url: str):
        """
        Register an internal timer when a crawl_website is called.
        """
        self._start_time = int(round(time.time() * 1000))
        self._current_url = url

    def execute(self) -> "page_soup":
        """
        Parsing url html to a bs4 soup object.
        """
        try:
            page_html = requests.get(
                self._current_url, headers=self._browser_header)
            print('         Accessing... {}'.format(self._current_url))
            page_soup = BeautifulSoup(page_html.content, 'html.parser')

            return page_soup
        except:
            raise Exception('Failed to reach this url.')