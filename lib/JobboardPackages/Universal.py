from abc import ABC, abstractmethod


class IJobboardSearch(ABC):
    @abstractmethod
    def search_board(self): pass

    @abstractmethod
    def search_job_description(self): pass


class UniversalSearch():
    def search_board(self):
        """
        Since it is a generic type, this method is empty and designed to be overwritten.
        """
        pass

    def search_job_description(self):
        """
        Just parse the entire website
        """
        pass
