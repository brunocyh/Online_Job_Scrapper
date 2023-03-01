from CrawlerService import Crawler
from DatabaseService.LocalSQLDatabase import JobDatabase

from CrawlerService.IndeedCrawler import IndeedSerach
from CrawlerService.SeekCrawler import SeekSerach
from CrawlerService import NeuvooSerach


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
