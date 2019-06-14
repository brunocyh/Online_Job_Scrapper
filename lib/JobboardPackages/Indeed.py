from lib.CrawlerService.Crawler import Crawler
from lib.DatabaseService.JobDBService import IJobDatabase
import time
import random


class IndeedSerach(UniversalSearch):

    def search_board(self, term, location):
        #  Job: indeed
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

        for index, page in enumerate(pages):

            # polite policy -- delay -- no dont make it static
            time.sleep(self.polite_policy_time_interval)

            # url processing
            k_words = term.replace(" ", "-")
            url = 'jobs?q={}&l={}&sort=date' + page
            url = domain + url.format(k_words, location)

            # html parsing
            page_soup = super.parsingHTML(url)

            # find all job titles
            containers = page_soup.findAll(
                "div", {"data-tn-component": "organicJob"})

            for job in containers:

                try:
                    # mapping
                    date = page
                    j_title = job.h2.text.strip()
                    company = job.findAll("span", {'class': 'company'})[
                        0].text.strip()
                    loc = job.findAll("span", {'class': 'location'})[
                        0].text.strip()
                    s_eng = b_name
                    term = term
                    u_link = domain + job.h2.a['href'].strip()
                    self.db.
                    list_jobs.add_data(date, j_title, company,
                                       loc, s_eng, term, u_link)

                except:
                    list_jobs.add_data(99, 'error', 'error',
                                       'error', s_eng, term, 'error')

            # Break if no result is returned from the first page
            if len(containers) == 0:
                if page == 0:
                    print("No result returned from {}, with term {}".format(
                        b_name, term))
                break

        return list_jobs.return_list()

    def search_job_description(self):
        """
        Indeed specific
        """
        pass