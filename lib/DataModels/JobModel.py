import hashlib

class JobModel():
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

    def get_id(self):
        h = hashlib.md5()
        txt = self.jobtitle + self.company + self.city
        h.update(txt.encode())
        return h.hexdigest()

    def _store_pkey(self):
        self.pkey = self.get_id()
