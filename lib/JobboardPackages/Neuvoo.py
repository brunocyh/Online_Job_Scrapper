from lib.CrawlerService.Crawler import Crawler
from lib.DataModels.JobModel import JobBuilder
from lib.JobboardPackages.Universal import UniversalSearch
import time
import random


class NeuvooSerach(UniversalSearch):

    domain = 'https://au.neuvoo.com/'
    b_name = 'Neuvoo'

    def search_board(self, term, place):
        pages = ['', '2', '3', '4', '5', '6']  # say, 30 results for indeed
        k_words = term.replace(" ", "+")

        for page in pages:

            # wait until the crawler is unlocked
            while self.crawler.is_locked():
                time.sleep(1)

            # Configure crawler only when cooled down
            url = 'jobs/?k={}&l={}&f=&o=&p={}&r=15'
            url = self.domain + url.format(k_words, place, page)
            cooldown_seconds = random.randint(10, 15)
            self.crawler.configure_crawler(url, cooldown_seconds)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # find all job titles
            containers = page_soup.findAll("div", {'class': 'job-c'})

            for p, job in enumerate(containers):

                try:
                    # TODO: to be tested
                    title = job.find('a', {'class': 'gojob'}).text
                    company = job.find('span', {'class': 'j-empname-label'}).text
                    location = job.find(
                        'div', {'class': 'j-location'}).findAll('span')[0].text
                    add_url = job.find('a', {'class': 'gojob'})[
                        'href'].strip('/')

                    job_builder = JobBuilder()
                    job_builder.set_jobtitle(title)
                    job_builder.set_company(company)
                    job_builder.set_location(location)
                    job_builder.set_city(place)
                    job_builder.set_search_engine(self.b_name)
                    job_builder.set_term(term)
                    job_builder.set_url(self.domain + add_url)

                    # Stores data only if it didnt exist
                    if not self.database.contains(job_builder.get_id()):
                        job_model = job_builder.build()
                        self.database.create_data(job_model)

                    else:
                        # data_id = job_builder.get_id()
                        # self.database.update_date(data_id)
                        pass

                except:
                    job_builder = JobBuilder()
                    job_model = job_builder.build_empty(term, self.b_name, place, self.domain + add_url)
                    self.database.create_data(job_model)

            # Unlock crawler
            self.crawler.unlock()

            # Break if no result is returned from the first page
            if len(containers) == 0:
                if page == 0:
                    print("No result returned from {}, with term {}".format(
                        self.b_name, term))
                break

        return True

    def search_job_description(self):
        """
        Indeed specific
        """
        pass
