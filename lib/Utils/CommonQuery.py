from lib.DatabaseService.LocalSQLDatabase import JobDatabase
from pandas import DataFrame


class CommonQuery:

    def get_jobs_within_2months(self):
        pass

    def get_jobs_custom(self):
        pass

    def get_jobs_all(self, columns: list):
        """
        For now we will just retrieve all the data.
        """
        data = []
        db = JobDatabase.instantiate_Database()
        db.connect()
        for result in db.read_all_data(columns):
            data.append(result)
        db.disconnect()
        return DataFrame(data, columns=columns)
