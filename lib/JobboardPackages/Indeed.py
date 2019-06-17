from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import IJobDatabase
import time
import random
from lib.CrawlerService.Crawler import ICrawler
from lib.DataModels.JobModel import JobBuilder


class IndeedSerach(UniversalSearch):

    crawler: ICrawler = None
    database: IJobDatabase = None

    def __init__(self, crawler: ICrawler):
        self.crawler = crawler

    def search_board(self, term, location):
        # TODO: not finished
        domain = 'https://au.indeed.com/'
        b_name = 'Indeed'
        pages = ['', '&start=10', '&start=20', '&start=30', '&start=40',
                 '&start=50', '&start=60']  # say, 30 results for indeed
        print('Now searching {} from {} ...'.format(term, b_name))

        # for each page:
        #   for each job in container:
        #       save in db + created date
        #   if duplicates more than 50%, stop crawling -> break

        for page in pages:

            # Configure crawler
            while not self.crawler.is_locked():
                try:
                    # url processing
                    k_words = term.replace(" ", "-")
                    url = 'jobs?q={}&l={}&sort=date' + page
                    url = domain + url.format(k_words, location)

                    # Polite Policy applies here
                    cooldown_seconds = random.randint(5, 8)

                    self.crawler.configure_crawler(url, cooldown_seconds)
                except:
                    time.sleep(1)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # find all job titles
            containers = page_soup.findAll(
                "div", {"data-tn-component": "organicJob"})

            for job in containers:

                try:
                    job_builder = JobBuilder()

                    # TODO: not impl
                    date = page

                    job_builder.set_jobtitle(job.h2.text.strip())
                    job_builder.set_company(job.findAll("span", {'class': 'company'})[
                        0].text)
                    job_builder.set_location(job.findAll("span", {'class': 'location'})[
                        0].text)
                    job_builder.set_search_engine(b_name)
                    job_builder.set_term(term)
                    job_builder.set_url(domain + job.h2.a['href'])

                    # Stores data only if it didnt exist
                    if not self.database.contains(job_builder.get_id()):
                        job_model = job_builder.build_empty()
                        self.database.create_data(job_model)

                except:
                    job_model = job_builder.build_empty()
                    self.database.create_data(job_model)

            # Break if no result is returned from the first page
            if len(containers) == 0:
                if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
                break

        return True

    def search_job_description(self):
        """
        Indeed specific
        """
        pass
