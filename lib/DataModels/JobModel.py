import hashlib


class JobModel():

    def __init__(self,
                 pkey,
                 page,
                 jobtitle,
                 company,
                 location,
                 city,
                 search_engine,
                 term,
                 url,
                 word_of_concerns):
        self.pkey = pkey
        self.page = page
        self.jobtitle = jobtitle
        self.company = company
        self.location = location
        self.city = city
        self.search_engine = search_engine
        self.term = term
        self.url = url
        self.word_of_concerns = word_of_concerns


class JobBuilder():

    pkey = ''
    page = ''
    jobtitle = ''
    company = ''
    location = ''
    city = ''
    search_engine = ''
    term = ''
    url = ''
    word_of_concerns = ''

    def set_page(self, content: str):
        self.page = content

    def set_jobtitle(self, content: str):
        self.jobtitle = content.lower().strip()

    def set_company(self, content: str):
        self.company = content.lower().strip()

    def set_location(self, content: str):
        self.location = content.lower().strip()
        
    def set_city(self, content: str):
        self.city = content.lower().strip()

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
            city=self.city,
            search_engine=self.search_engine,
            term=self.term,
            url=self.url,
            word_of_concerns=self.word_of_concerns
        )

    def build_empty(self, term='404', engine='404', city='404', url='404'):
        h = hashlib.md5()
        txt = term+engine+city+url
        h.update(txt.encode())
        return JobModel(
            pkey=h.hexdigest(),
            page='404',
            jobtitle='404',
            company='404',
            location='404',
            city=city,
            search_engine=engine,
            term=term,
            url=url,
            word_of_concerns='404'
        )

    def get_id(self):
        h = hashlib.md5()
        txt = self.jobtitle+self.company+self.city+self.url
        h.update(txt.encode())
        return h.hexdigest()

    def _store_pkey(self):
        self.pkey = self.get_id()
