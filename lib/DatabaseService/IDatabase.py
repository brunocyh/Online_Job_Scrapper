from abc import ABC, abstractmethod

from lib.DataModels.JobModel import JobModel


class IDatabase(ABC):

    @abstractmethod
    def create(self, jobModel: JobModel):
        pass

    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def update(self, jobModel: JobModel):
        pass

    @abstractmethod
    def delete(self, job_id: str):
        pass

    @abstractmethod
    def contains(self, job_id: str):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def commit(self):
        pass
