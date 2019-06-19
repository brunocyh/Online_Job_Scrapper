from abc import ABC, abstractmethod
import sqlite3
from lib.DataModels.JobModel import JobModel
import time


"""
If we want to expand this service, we might need to consider using command design pattern. Dont really know how i can impl yet.
"""


class IJobDatabase(ABC):
    @staticmethod
    def instantiate_Database(): pass

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass

    @abstractmethod
    def commit(self): pass

    @abstractmethod
    def reset_table(self, passcode): pass

    @abstractmethod
    def create_data(self, key_pair: dict): pass

    @abstractmethod
    def read_all_data(self, columns): pass

    @abstractmethod
    def update_analysed_data(self, conditions: tuple, key_pair: tuple): pass

    @abstractmethod
    def delete_data(self): pass


class JobDatabase(IJobDatabase):

    # Singleton DB
    __instance = None
    conn = None
    cursor = None
    db_name = "Database/Job.db"
    table_name = "job_table"
    passcode = "4321"
    created_time = time.time()

    @staticmethod
    def instantiate_Database() -> IJobDatabase:
        if JobDatabase.__instance == None:
            JobDatabase()
        return JobDatabase.__instance

    def __init__(self):
        # singleton
        if JobDatabase.__instance != None:
            raise Exception('DB is a singleton obejct')

        else:
            JobDatabase.__instance = self

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
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
        cmd.append("CREATE TABLE {} (PKey text, Page text, Job_title text, Company text, Location text, Search_eng text,\
            Term text, URL text, Words_of_concern text, created_time Integer)".format(self.table_name))

        [self._sql(c) for c in cmd]
        return True

    def _sql(self, sql):
        return self.cursor.execute(sql)

    def create_data(self, job_model: JobModel):
        try:
            cmd = "INSERT INTO {} VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(self.table_name,
                                                                                                     job_model.pkey,
                                                                                                     job_model.page,
                                                                                                     job_model.jobtitle,
                                                                                                     job_model.company,
                                                                                                     job_model.location,
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

    def update_analysed_data(self, conditions: tuple, key_pair: tuple):
        try:
            cmd = "UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(self.table_name,
                                                                    conditions[0],
                                                                    conditions[1],
                                                                    key_pair[0],
                                                                    key_pair[1])
            self._sql(cmd)
            return True

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
            cmd = "Select 1 FROM {} WHERE EXISTS (SELECT 1 FROM {} WHERE pkey = '{}');".format(
                self.table_name, self.table_name, job_id)
            cursor = self._sql(cmd)

            if cursor.rowcount <= 0:
                return False
            else:
                return True

        except Exception as e:
            raise e

    # TODO: Further development
    def delete_data(self):
        raise Exception('Not implemented error')
