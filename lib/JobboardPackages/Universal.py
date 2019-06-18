from lib.DatabaseService.JobDBService import IJobDatabase
from lib.CrawlerService.Crawler import ICrawler
from abc import ABC, abstractmethod


class IJobboardSearch(ABC):
    @abstractmethod
    def search_board(self): pass

    @abstractmethod
    def search_job_description(self): pass


class UniversalSearch():

    crawler: ICrawler = None
    database: IJobDatabase = None

    def __init__(self, crawler, database):
        self.crawler = crawler
        self.database = database

    def search_board(self):
        """
        Since it is a generic type, this method is empty and designed to be overwritten.
        """
        pass

    def search_job_description(self):
        """
        Just parse the entire website
        """
        pass
