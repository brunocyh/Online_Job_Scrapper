import hashlib
from datetime import time


class JobModel:
    def __init__(self):
        self.jobtitle = None
        self.term = None
        self.city = None
        self.location = None
        self.company = None
        self.page = None
        self.url = None
        self.word_of_concerns = None
        self.search_engine = None
        self.last_update_date = None
        self.post_date = None

    def set_page(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.page = clean_content

    def set_jobtitle(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.jobtitle = clean_content.lower().strip()

    def set_company(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.company = clean_content.lower().strip()

    def set_location(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.location = clean_content.lower().strip()

    def set_city(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.city = clean_content.lower().strip()

    def set_search_engine(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.search_engine = clean_content

    def set_term(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.term = clean_content.lower().strip()

    def set_url(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.url = clean_content.strip()

    def set_word_of_concerns(self, content: str):
        clean_content = self._sanitize_str_data(content)
        self.word_of_concerns = clean_content

    def set_post_date(self, unix_date: int):
        if type(unix_date) is int:
            self.post_date = unix_date

        else:
            self.post_date = "DATE FORMAT ERR"

    def get_id(self) -> str:
        h = hashlib.md5()
        txt = self.jobtitle + self.company + self.search_engine
        h.update(txt.encode())
        return h.hexdigest()

    def _sanitize_str_data(self, content: str):
        # Empty Data
        if content == "":
            return "NO DATA"

        # Data Not filled
        if content is None:
            return "NOT FILLED"

        # Type check
        if type(content) is not str:
            return "FORMAT ERR"

    def _update_time(self):
        # Update timestamp
        self.last_update_date = time.time()
