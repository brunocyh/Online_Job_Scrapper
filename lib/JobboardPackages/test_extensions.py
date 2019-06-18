from lib.JobboardPackages.Indeed import IndeedSerach
from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import JobDatabase


def test_integration_indeed():
    crawler = Crawler()

    database = JobDatabase.instantiate_Database()
    database.connect()
    searcher = IndeedSerach(crawler, database)
    response = searcher.search_board(term='barista', location='brisbane')

    database.commit()
    database.disconnect()
    assert response == True
