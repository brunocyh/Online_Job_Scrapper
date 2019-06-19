from lib.DatabaseService.JobDBService import JobDatabase
from pandas import DataFrame


class Query():

    def get_jobs_within_2months(self):
        pass

    def get_jobs_custom(self):
        pass

    def get_jobs_all(self):
        #TODO: tb tested
        data = []
        db = JobDatabase.instantiate_Database()
        db.connect()
        for result in db.read_all_data():
            data.append(result)
        db.disconnect()
        return DataFrame(data)
