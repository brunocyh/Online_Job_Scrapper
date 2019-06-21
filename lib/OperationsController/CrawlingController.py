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
    terms = []
    locations = []
    prefix = []
    stop_words = []
    # words_of_concerns = []

    def __init__(self, terms: list, locations: list,
                 prefix: list = [], stop_words: list = [],
                 words_of_concerns: list = []):
        self.db_instance = JobDatabase.instantiate_Database()
        self.terms = terms
        self.locations = locations
        self.prefix = prefix
        self.stop_words = stop_words
        # self.words_of_concerns=words_of_concerns

    def execute(self) -> list:
        """
        So after the execusion of the search, user should expect all the information crawled are
        stored in the database. Terefore user should us Query Controllers to retrieve any results.
        This method returns a list of critical logs occured during the exploration on internet.
        """
        # Switch on DB
        self.db_instance.connect()

        # Construct differnt combination of words
        search_terms = []
        for place in self.locations:
            for pfx in self.prefix:
                for trm in self.terms:
                    searach_object = (place, pfx + " " + trm)
                    search_terms.append(searach_object)

        # Config each crawler, attach engines to each thread (for each search term)
        for indx, pair in enumerate(search_terms):
            threads = []
            location, search_term = pair
            for instance in self.engines:
                new_thread = self._configure_thread(instance, search_term, location)
                threads.append(new_thread)

            # Run threads (Start engine and wait till they re done)
            self._start_all_threads(threads)
            progress = (indx+1) * 100 / len(search_terms)
            print('[{}%] Now searching {} in {}'.format(progress, search_term, location))
            self._await_all_threads(threads)

        # Switch off DB
        self.db_instance.disconnect()

        # Report Generation:
        return self.errors

    def _configure_thread(self, instance, term, location):
        crawler_instance = Crawler()
        engine: IJobboardSearch = instance(crawler=crawler_instance,
                                           database=self.db_instance)

        # Create thread
        crawler_thread = threading.Thread(
            target=SearchEngine._thread_crawler, args=(engine, engine.b_name, term, location,), daemon=True)

        # Attach to thread list
        return crawler_thread

    def _start_all_threads(self, threads):
        for thread in threads:
            thread.start()

    def _await_all_threads(self, threads):
        for thread in threads:
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
