import requests
from bs4 import BeautifulSoup
import time

from abc import ABC, abstractmethod


class ICrawler(ABC):

    @abstractmethod
    def configure_crawler(self, url: str, crawler_freeze_seconds: int):
        pass

    @abstractmethod
    def execute(self) -> "page_soup":
        pass

    @abstractmethod
    def is_locked(self) -> bool:
        pass

    @abstractmethod
    def unlock(self) -> bool:
        pass
    
    @abstractmethod
    def cooldown_time(self) -> bool:
        pass


class Crawler():
    """
    Crawler is intended to be instantiated once per domain. It supports 
    mechanism that make sure it crawl politely.
    """
    _browser_header = {'User-Agent': "Mozilla/5.0 (X11; Linux i686; rv:64.0) \
                      Gecko/20100101 Firefox/64.0"}
    _current_url = None
    _start_time = 0
    _crawler_freeze_seconds = 0

    def configure_crawler(self, url: str, crawler_freeze_seconds: int):
        """
        Register an internal timer when a crawl_website is called.
        """
        if self.is_locked():
            raise Exception('This crawler is locked')

        self._start_time = int(round(time.time() * 1000))
        self._current_url = url
        self._crawler_freeze_seconds = crawler_freeze_seconds

    def execute(self) -> "page_soup":
        """
        Parsing url html to a bs4 soup object.
        """
        try:
            page_html = requests.get(
                self._current_url, headers=self._browser_header)
            print('internet accessing... {}'.format(self._current_url))
            page_soup = BeautifulSoup(page_html.content, 'html.parser')

            self._register_as_used()
            return page_soup
        except:
            raise Exception('Failed to reach this url.')

    def is_locked(self) -> bool:
        """
        Check whether the current time is n seconds after starting time.
        """
        unlockable_time = self._start_time + \
            (self._crawler_freeze_seconds * 1000)
        now = int(round(time.time() * 1000))
        if now < unlockable_time or self._current_url != None:
            return True
        else:
            return False

    def cooldown_time(self):
        unlockable_time = self._start_time + \
            (self._crawler_freeze_seconds * 1000)
        now = int(round(time.time() * 1000))
        return unlockable_time - now

    def _register_as_used(self):
        self._current_url = ''
        
    def unlock(self):
        self._current_url = None
