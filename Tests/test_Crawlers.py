from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import JobDatabase

from lib.CrawlerService.IndeedCrawler import IndeedSerach
from lib.CrawlerService.SeekCrawler import SeekSerach
from lib.CrawlerService.Neuvoo import NeuvooSerach


def test_integration_indeed():
    crawler = Crawler()

    database = JobDatabase.instantiate_Database()
    database.connect()
    searcher = IndeedSerach(crawler, database)
    response = searcher.search_board(term='barista', location='brisbane')

    database.commit()
    database.disconnect()
    assert response == True


def test_integration_seek():
    crawler = Crawler()

    database = JobDatabase.instantiate_Database()
    database.connect()
    searcher = SeekSerach(crawler, database)
    response = searcher.search_board(term='barista', location='brisbane')

    database.commit()
    database.disconnect()
    assert response == True


def test_integration_neuvoo():
    crawler = Crawler()

    database = JobDatabase.instantiate_Database()
    database.connect()
    searcher = NeuvooSerach(crawler, database)
    response = searcher.search_board(term='barista', location='brisbane')

    database.commit()
    database.disconnect()
    assert response == True
