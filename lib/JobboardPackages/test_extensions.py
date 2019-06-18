from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import JobDatabase

from lib.JobboardPackages.Indeed import IndeedSerach
from lib.JobboardPackages.Seek import SeekSerach
from lib.JobboardPackages.Neuvoo import NeuvooSerach
from lib.JobboardPackages.Gumtree import GumtreeSerach


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


# def test_integration_neuvoo():
#     crawler = Crawler()

#     database = JobDatabase.instantiate_Database()
#     database.connect()
#     searcher = NeuvooSerach(crawler, database)
#     response = searcher.search_board(term='barista', location='brisbane')

#     database.commit()
#     database.disconnect()
#     assert response == True


# def test_integration_gumtree():
#     crawler = Crawler()

#     database = JobDatabase.instantiate_Database()
#     database.connect()
#     searcher = GumtreeSerach(crawler, database)
#     response = searcher.search_board(term='barista', location='brisbane')

#     database.commit()
#     database.disconnect()
#     assert response == True
