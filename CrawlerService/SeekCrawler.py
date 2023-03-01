from CrawlerService.CrawlerThread import CrawlerThread
from DataModels.JobModel import JobModel


class SeekCrawler(CrawlerThread):
    domain = 'https://www.seek.com.au/'
    b_name = 'Seek'

    def return_url_list(self) -> "list(String)":
        # Example
        # ["jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=10",
        # "jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=20",
        # ...]

        pages = ['', '&page=2', '&page=3', '&page=4', '&page=5',
                 '&page=6', '&page=7']  # say, 30 results for indeed

        url_list = []

        # Construct list of url_extensions
        for page in pages:
            for k_word in self.keywords:
                extension = '{}-jobs/in-{}?sortmode=ListedDate'.format(k_word, self.place) + page
                url_list.append(extension)

        return url_list

    def return_list_of_jobs(self, page_soup) -> "list(JobModel)":
        # BeautifulSoup page_soup

        # Example
        containers = page_soup.findAll("article")

        for p, job in enumerate(containers):
            add_url = job.find(
                'a', {'data-automation': 'jobTitle'})['href'].strip('/')
            company = job.find(
                'a', {'data-automation': 'jobCompany'}).text
            title = job.find(
                'a', {'data-automation': 'jobTitle'}).text
            location = job.find(
                'a', {'data-automation': 'jobArea'}).text

            # Build a Job object
            model = JobModel()
            model.set_jobtitle(title)
            model.set_company(company)
            model.set_location(location)
            model.set_search_engine(self.b_name)
            model.set_url(self.domain + add_url)
