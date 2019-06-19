import logging
import threading
import time

from lib.JobboardPackages.Universal import IJobboardSearch
from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import JobDatabase

from lib.JobboardPackages.Seek import SeekSerach
from lib.JobboardPackages.Indeed import IndeedSerach
from lib.JobboardPackages.Neuvoo import NeuvooSerach


class SearchEngine():

    # Engines
    db_instance = None
    engines = [SeekSerach, IndeedSerach, NeuvooSerach]
    threads = []

    # Parameters
    term = None
    location = None

    def __init__(self, term, location):
        self.db_instance = JobDatabase()
        self.term = term
        self.location = location

    def search_internet(self):
        # TODO: tb tested
        """
        Algorithm:
        - create threads //
        - run threads parallel  //
        - await all threads return True / Exceptions //
        - create report for this run ??
        - end
        """
        # Switch on DB
        self.db_instance.connect()

        try:
            # Config each crawler, attach engines to each thread
            for instance in self.engines:
                self._configure_thread(instance)

            # Run threads (Start engine and wait till they re done)
            self._start_all_threads()
            self._await_all_threads()

        except Exception as e:
            raise Exception("Tread error: " + str(e))

        finally:
            # Report Generation:
            pass

            # Switch off DB
            self.db_instance.disconnect()

    def _configure_thread(self, instance):
        crawler_instance = Crawler()
        engine = instance(crawler=crawler_instance,
                          database=self.db_instance)

        # Create thread
        crawler_thread = threading.Thread(
            target=SearchEngine._thread_crawler, args=(engine, self.term, self.location,), daemon=True)

        # Attach to thread list
        self.threads.append(crawler_thread)

    def _start_all_threads(self):
        for thread in self.threads:
            thread.start()

    def _await_all_threads(self):
        for thread in self.threads:
            thread.join()

    @staticmethod
    def _thread_crawler(crawler: IJobboardSearch, term: str, location: str):
        try:
            return crawler.search_board(term, location)

        except Exception as e:
            raise Exception('Thread {} has issue: {}'.format('n/a', str(e)))
