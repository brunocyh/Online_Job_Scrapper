from abc import ABC, abstractmethod
from threading import Thread
import time
import random
import Crawler


class CrawlerThread(ABC, Thread):

    def __init__(self, thread_id, url_domain):
        self.thread_id = thread_id
        self.url_domain = url_domain
        self.crawler = Crawler()

        # Instaniate myself
        Thread.__init__(self)

        # Create Temporary Database for this crawler
        self.job_data = dict()

    @abstractmethod
    def return_url_list(self) -> "list(String)":
        # Example
        # ["jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=10",
        # "jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=20",
        # ...]
        pass

    @abstractmethod
    def return_list_of_jobs(self, page_soup) -> "list(JobModel)":
        # BeautifulSoup page_soup

        # Example
        # containers = page_soup.findAll(
        #    "div", {"data-tn-component": "organicJob"})
        pass

    def run(self):

        # Get a list of url extention
        url_extentions = self.return_url_extension_list()

        # Iterate through the custom URL parameters
        for url_extension in url_extentions:

            # Pause (Web crawling Polite policy)
            time.sleep(random.randint(10, 15))

            # Configure crawler URl
            url = self.url_domain + url_extension

            # Prepare crawler
            self.crawler.configure_crawler(url)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # Get a list of jobs from BS4
            jobs_objects = self.return_list_of_jobs(page_soup)

            # Logic gate to skip empty page
            if len(jobs_objects) == 0:
                break

            # Store jobs to temp DB (Panda?)
            for p, job in enumerate(jobs_objects):
                # Update data only if it hasn't been found before
                self.job_data.update({job.get_id(), job})

        return True
