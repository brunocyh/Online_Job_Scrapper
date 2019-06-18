from lib.CrawlerService.Crawler import Crawler
from lib.DataModels.JobModel import JobBuilder
from lib.JobboardPackages.Universal import UniversalSearch
import time
import random


class GumtreeSerach(UniversalSearch):

    domain = 'https://www.gumtree.com.au/'
    b_name = 'Gumtree'

    def search_board(self, term, location):
        print('Now searching {} from {} ...'.format(term, self.b_name))

        pages = ['', 'page-2/', 'page-3/', 'page-4/',
                 'page-5/']  # say, 30 results for indeed
        k_words = term.replace(" ", "-")

        for page in pages:

            # wait until the crawler is unlocked
            while self.crawler.is_locked():
                time.sleep(1)

            # Configure crawler only when cooled down
            # TODO: sure?? but nvm gumtree is not too useful
            url = '/s-jobs/{}/{}/{}k0c9302l3005721?sort=rank&ad=offering'
            url = self.domain + url.format(location, k_words, page)
            cooldown_seconds = random.randint(5, 8)
            self.crawler.configure_crawler(url, cooldown_seconds)

            # Retrieve web page
            page_soup = self.crawler.execute()

            # find all job titles
            containers = page_soup.findAll(
                'a', {'class': 'user-ad-row user-ad-row--no-image link link--base-color-inherit link--hover-color-none link--no-underline'})

            for p, job in enumerate(containers):

                try:
                    # TODO: to be confirmed
                    job_builder = JobBuilder()
                    job_builder.set_jobtitle(
                        job.find('div', {'class': 'title'}).a['title'])
                    job_builder.set_company(
                        job.find('div', {'class': 'sjcl'}).div.span.text.strip())
                    job_builder.set_location(
                        job.find('div', {'class': 'sjcl'}).findAll('span')[1].text)
                    job_builder.set_search_engine(self.b_name)
                    job_builder.set_term(term)
                    job_builder.set_url(
                        self.domain + job.find('div', {'class': 'title'}).a['href'].strip('/'))

                    # Stores data only if it didnt exist
                    if not self.database.contains(job_builder.get_id()):
                        job_model = job_builder.build()
                        self.database.create_data(job_model)

                    else:
                        # data_id = job_builder.get_id()
                        # self.database.update_date(data_id)
                        pass

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
