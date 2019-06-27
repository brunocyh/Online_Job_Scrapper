from lib.OperationsController.CrawlingController import SearchEngine
from lib.OperationsController.QueryController import Query


# TODO:  not tested and bad test
def test_crawler_search_engine():
    engine = SearchEngine(term='barista', location='brisbane')
    assert type(engine.execute()) == list


# TODO:  not tested and bad test
def test_crawler_query():
    engine = Query()
    engine.get_jobs_all()
    assert True
