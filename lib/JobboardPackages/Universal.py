from lib.DatabaseService.JobDBService import IJobDatabase
from lib.CrawlerService.Crawler import ICrawler
from abc import ABC, abstractmethod


class IJobboardSearch(ABC):
    @abstractmethod
    def search_board(self, term, location): pass

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
    
    def searching_algorithm_jobs(self):
        """
        Only be used for child
        """
        #TODO: refactor different crawlers: they should inherit this method
        pass
