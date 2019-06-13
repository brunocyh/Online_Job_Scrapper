class JobModel():

    def __init__(self, 
                 page,
                 jobtitle,
                 company,
                 location,
                 search_engine,
                 term,
                 url,
                 word_of_concerns):
        self.page = page
        self.jobtitle = jobtitle
        self.company = company
        self.location = location
        self.search_engine = search_engine
        self.term = term
        self.url = url
        self.word_of_concerns = word_of_concerns


class JobBuilder():

    page = None
    jobtitle = None
    company = None
    location = None
    search_engine = None
    term = None
    url = None
    word_of_concerns = None

    def set_page(self, content: str):
        self.page = content

    def set_jobtitle(self, content: str):
        self.jobtitle = content

    def set_company(self, content: str):
        self.company = content

    def set_location(self, content: str):
        self.location = content

    def set_search_engine(self, content: str):
        self.search_engine = content

    def set_term(self, content: str):
        self.term = content

    def set_url(self, content: str):
        self.url = content

    def set_word_of_concerns(self, content: str):
        self.word_of_concerns = content

    def get_job(self):
        # TODO: to be implm, do i need to check whether all attr arte filled?
        raise Exception('Not implm error')
