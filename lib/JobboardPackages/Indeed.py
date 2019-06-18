from lib.CrawlerService.Crawler import Crawler
from lib.DataModels.JobModel import JobBuilder
from lib.JobboardPackages.Universal import UniversalSearch
import time
import random


class IndeedSerach(UniversalSearch):
    
    domain = 'https://au.indeed.com/'
    b_name = 'Indeed'

    def search_board(self, term, location):
        print('Now searching {} from {} ...'.format(term, self.b_name))
        
        pages = ['', '&start=10', '&start=20', '&start=30', '&start=40',
                 '&start=50', '&start=60']  # say, 30 results for indeed
        k_words = term.replace(" ", "-")

        for page in pages:

            # wait until the crawler is unlocked
            while self.crawler.is_locked():
                time.sleep(1)

            # Configure crawler only when cooled down
            url = 'jobs?q={}&l={}&sort=date' + page
            url = self.domain + url.format(k_words, location)
            cooldown_seconds = random.randint(5, 8)
            self.crawler.configure_crawler(url, cooldown_seconds)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # find all job titles
            containers = page_soup.findAll(
                "div", {"data-tn-component": "organicJob"})

            for job in containers:

                try:
                    job_builder = JobBuilder()
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

                    else:
                        data_id = job_model.get_id()
                        self.database.update_date(data_id)

                except:
                    job_model = job_builder.build_empty()
                    self.database.create_data(job_model)

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
