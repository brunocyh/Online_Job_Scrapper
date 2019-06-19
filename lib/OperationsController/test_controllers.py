from lib.OperationsController.CrawlingController import SearchEngine


# TODO: not run yet
def test_crawler_search_engine():
    engine = SearchEngine(term='barista', location='brisbane')
    engine.execute()
