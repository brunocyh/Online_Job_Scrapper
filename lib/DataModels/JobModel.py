import hashlib


class JobModel():

    def __init__(self,
                 pkey,
                 page,
                 jobtitle,
                 company,
                 location,
                 search_engine,
                 term,
                 url,
                 word_of_concerns):
        self.pkey = pkey
        self.page = page
        self.jobtitle = jobtitle
        self.company = company
        self.location = location
        self.search_engine = search_engine
        self.term = term
        self.url = url
        self.word_of_concerns = word_of_concerns


class JobBuilder():

    pkey = None
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
        self.company = content.lower().strip()

    def set_location(self, content: str):
        self.location = content.lower().strip()

    def set_search_engine(self, content: str):
        self.search_engine = content

    def set_term(self, content: str):
        self.term = content.lower().strip()

    def set_url(self, content: str):
        self.url = content.strip()

    def set_word_of_concerns(self, content: str):
        self.word_of_concerns = content

    def build(self):
        self._store_pkey()
        return JobModel(
            pkey=self.pkey,
            page=self.page,
            jobtitle=self.jobtitle,
            company=self.company,
            location=self.location,
            search_engine=self.search_engine,
            term=self.term,
            url=self.url,
            word_of_concerns=self.word_of_concerns
        )

    def build_empty(self):
        self._store_pkey()
        return JobModel(
            pkey=self.pkey,
            page='404',
            jobtitle='404',
            company='404',
            location='404',
            search_engine='404',
            term='404',
            url='404',
            word_of_concerns='404'
        )

    def get_job(self):
        # TODO: to be implm, do i need to check whether all attr arte filled?
        raise Exception('Not implm error')

    def get_id(self):
        h = hashlib.md5()
        txt = self.company+self.url
        h.update(txt.encode())
        return h.hexdigest()

    def _store_pkey(self):
        self.pkey = self.get_id()
