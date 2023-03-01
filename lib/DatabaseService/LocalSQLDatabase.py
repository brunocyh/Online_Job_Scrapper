from abc import ABC, abstractmethod
import sqlite3
from lib.DataModels.JobModel import JobModel
import time

from lib.DatabaseService.IDatabase import IDatabase

"""
If we want to expand this service, we might need to consider using command design pattern. Dont really know how i can impl yet.
"""


class LocalSQLDatabase(IDatabase):

    def __init__(self):
        self.DB_SCHEMA = "(PKey text PRIMARY KEY, " \
                         "Page text, " \
                         "Job_title text, " \
                         "Company text, " \
                         "Location text, " \
                         "City text, " \
                         "Search_eng text," \
                         "Term text, " \
                         "URL text, " \
                         "Words_of_concern text, " \
                         "created_time Integer)"

        # Singleton DB
        self.__instance = None
        self.conn = None
        self.cursor = None

        # TODO: Refactor to secure place later
        self.db_name = "Database/Job.db"
        self.table_name = "job_table"
        self.passcode = "4321"
        self.created_time = int(time.time())

        # Singleton Pattern
        if LocalSQLDatabase.__instance != None:
            raise Exception('DataBase is already instantiated.')

        else:
            LocalSQLDatabase.__instance = self

    @staticmethod
    def get_database_instance() -> IDatabase:
        if LocalSQLDatabase.__instance == None:
            LocalSQLDatabase()
        return LocalSQLDatabase.__instance

    def create(self, job_model: JobModel):
        try:
            cmd = "INSERT INTO {} VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                self.table_name,
                job_model.pkey,
                job_model.page,
                job_model.jobtitle,
                job_model.company,
                job_model.location,
                job_model.city,
                job_model.search_engine,
                job_model.term,
                job_model.url,
                job_model.word_of_concerns,
                self.created_time
            )
            self._sql(cmd)
            return True

        except Exception as e:
            raise e

    def update(self, job_model: JobModel):
        try:

            """
            1. Get the job_id of the job from DB
            2. Check its last update
            3. if this is re-posted, then renew its date
            """

            cmd = "UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(self.table_name,
                                                                    conditions[0],
                                                                    conditions[1],
                                                                    key_pair[0],
                                                                    job_model.get_id())
            self._sql(cmd)
            return True

        except Exception as e:
            raise e

    def delete(self, job_id: str):
        pass

    def connect(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        return True

    def disconnect(self):
        self.conn.commit()
        self.conn.close()
        return True

    def commit(self):
        self.conn.commit()
        return True

    def reset_table(self, passcode):
        print('I hope you know what you are doing...')
        if passcode != self.passcode:
            raise Exception('Wrong password, db reset request declined')
        cmd = []
        cmd.append("DROP TABLE IF EXISTS {};".format(self.table_name))
        cmd.append("CREATE TABLE {} ".format(self.table_name) + self.DB_SCHEMA)

        [self._sql(c) for c in cmd]
        return True

    def read_all_data(self, columns: "list of strings") -> "iterator":
        try:
            columns_str = ""
            for counter, word in enumerate(columns):
                if counter >= 1:
                    columns_str = columns_str + ", " + word

                else:
                    columns_str = word

            cmd = "SELECT {} FROM {}".format(columns_str, self.table_name)
            return self._sql(cmd)

        except Exception as e:
            raise e

    def update_date(self, data_id: str):
        try:
            cmd = "UPDATE {} SET created_time = '{}' WHERE pkey = '{}';".format(self.table_name,
                                                                                self.created_time,
                                                                                data_id)
            self._sql(cmd)
            return True

        except Exception as e:
            raise e

    def contains(self, job_id: str):

        try:
            cmd = "SELECT 1 FROM {} WHERE pkey = '{}';".format(
                self.table_name, job_id)
            results = self._sql(cmd).fetchall()

            if len(results) <= 0:
                return False
            else:
                return True

        except Exception as e:
            raise e

    # TODO: Further development
    def delete_data(self):
        raise Exception('Not implemented error')

    def _sql(self, sql: str):
        return self.cursor.execute(sql)
