from CrawlerService.CrawlerThread import CrawlerThread
from DataModels.JobModel import JobModel


class IndeedCrawler(CrawlerThread):
    domain = 'https://au.indeed.com/'
    b_name = 'Indeed'

    def __init__(self, keywords: list, place: str):
        self.keywords = keywords
        self.place = place

    def return_url_list(self) -> "list(String)":
        # Example
        # ["jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=10",
        # "jobs?q=SoftwareEngineer&l=Dubai&sort=date&start=20",
        # ...]

        pages = ['', '&start=10', '&start=20', '&start=30', '&start=40',
                 '&start=50', '&start=60']  # say, 30 results for indeed

        url_list = []

        # Construct list of url_extensions
        for page in pages:
            for k_word in self.keywords:
                extension = 'jobs?q={}&l={}&sort=date'.format(k_word, self.place) + page
                url_list.append(extension)

        return url_list

    def return_list_of_jobs(self, page_soup) -> "list(JobModel)":
        # BeautifulSoup page_soup

        # Example
        containers = page_soup.findAll("div", {"data-tn-component": "organicJob"})

        for p, job in enumerate(containers):
            add_url = job.find(
                'div', {'class': 'title'}).a['href'].strip('/')
            company = job.find(
                'div', {'class': 'sjcl'}).div.span.text.strip()
            title = job.find('div', {'class': 'title'}).a['title']
            location = job.find(
                'div', {'class': 'sjcl'}).findAll('span')[1].text

            # Build a Job object
            model = JobModel()
            model.set_jobtitle(title)
            model.set_company(company)
            model.set_location(location)
            model.set_search_engine(self.b_name)
            model.set_url(self.domain + add_url)
