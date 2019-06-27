from lib.CrawlerService.Crawler import Crawler
from lib.DataModels.JobModel import JobBuilder
from lib.JobboardPackages.Universal import UniversalSearch
import time
import random


class SeekSerach(UniversalSearch):

    domain = 'https://www.seek.com.au/'
    b_name = 'Seek'

    def search_board(self, term, place):
        pages = ['', '&page=2', '&page=3', '&page=4', '&page=5',
                 '&page=6', '&page=7']  # say, 30 results for indeed
        k_words = term.replace(" ", "-")

        for page in pages:

            # wait until the crawler is unlocked
            while self.crawler.is_locked():
                time.sleep(1)

            # Configure crawler only when cooled down
            url = '{}-jobs/in-{}?sortmode=ListedDate' + page
            url = self.domain + url.format(k_words, place)
            cooldown_seconds = random.randint(10, 15)
            self.crawler.configure_crawler(url, cooldown_seconds)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # find all job titles
            containers = page_soup.findAll("article")

            for p, job in enumerate(containers):

                try:
                    add_url = job.find(
                        'a', {'data-automation': 'jobTitle'})['href'].strip('/')
                    company = job.find(
                        'a', {'data-automation': 'jobCompany'}).text
                    title = job.find(
                        'a', {'data-automation': 'jobTitle'}).text
                    location = job.find(
                        'a', {'data-automation': 'jobArea'}).text

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
                    job_model = job_builder.build_empty(
                        term, self.b_name, place, self.domain + add_url)
                    self.database.create_data(job_model)

                finally:
                    self.database.commit()

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
