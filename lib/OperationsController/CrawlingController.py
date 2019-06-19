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
    errors = []

    # Parameters
    term = None
    location = None

    def __init__(self, term, location):
        self.db_instance = JobDatabase.instantiate_Database()
        self.term = term
        self.location = location

    def execute(self) -> list:
        """
        So after the execusion of the search, user should expect all the information crawled are
        stored in the database. Terefore user should us Query Controllers to retrieve any results.
        This method returns a list of critical logs occured during the exploration on internet.
        """
        # Switch on DB
        self.db_instance.connect()

        # Config each crawler, attach engines to each thread
        for instance in self.engines:
            self._configure_thread(instance)

        # Run threads (Start engine and wait till they re done)
        self._start_all_threads()
        self._await_all_threads()

        # Switch off DB
        self.db_instance.disconnect()

        # Report Generation:
        return self.errors

    def _configure_thread(self, instance):
        crawler_instance = Crawler()
        engine: IJobboardSearch = instance(crawler=crawler_instance,
                                           database=self.db_instance)

        # Create thread
        crawler_thread = threading.Thread(
            target=SearchEngine._thread_crawler, args=(engine, engine.b_name, self.term, self.location,), daemon=True)

        # Attach to thread list
        self.threads.append(crawler_thread)

    def _start_all_threads(self):
        for thread in self.threads:
            thread.start()

    def _await_all_threads(self):
        for thread in self.threads:
            try:
                thread.join()

            except Exception as e:
                self.errors.append(str(e))

    @staticmethod
    def _thread_crawler(crawler: IJobboardSearch, eng_name: str, term: str, location: str):
        try:
            return crawler.search_board(term, location)

        except Exception as e:
            raise Exception('Thread {} has issue: {}'.format(eng_name, str(e)))
