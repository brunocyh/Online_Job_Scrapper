from lib.JobboardPackages.Indeed import IndeedSerach
from lib.CrawlerService.Crawler import Crawler


# TODO: test failed still
def test_integration_indeed():
    crawler = Crawler()
    searcher = IndeedSerach(crawler)

    assert searcher.search_board(term='software engineer', location='brisbane')
