from lib.CrawlerService.Crawler import Crawler
import time


def test_crawler():
    crawler = Crawler()
    assert not crawler.is_locked()
    crawler.configure_crawler(url = "https://hk.yahoo.com/", crawler_freeze_seconds=1)
    
    assert crawler.is_locked()
    crawler.execute()
    
    time.sleep(2)
    assert not crawler.is_locked()