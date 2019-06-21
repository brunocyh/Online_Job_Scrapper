from lib.DatabaseService.JobDBService import JobDatabase
from pandas import DataFrame


class Query():

    def get_jobs_within_2months(self):
        pass

    def get_jobs_custom(self):
        pass

    def get_jobs_all(self):
        """
        For now we will just retrieve all the data.
        """
        data = []
        db = JobDatabase.instantiate_Database()
        db.connect()
        columns = ["PKey", "Job_title", "Company", "Location", "City", "Search_eng", "Term", "URL", "Words_of_concern", "created_time"]
        for result in db.read_all_data(columns):
            data.append(result)
        db.disconnect()
        return DataFrame(data, columns=columns)
