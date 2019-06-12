from abc import ABC, abstractmethod
import sqlite3


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
    def reset_table(self): pass

    @abstractmethod
    def create_data(self): pass

    @abstractmethod
    def read_all_data(self, columns): pass

    @abstractmethod
    def update_data(self): pass

    @abstractmethod
    def delete_data(self): pass


class JobDatabase(IJobDatabase):

    __instance = None
    conn = None
    cursor = None
    db_name = "Job.db"
    table_name = "job_table"

    @staticmethod
    def instantiate_Database():
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

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def reset_table(self):
        # TODO: to be continued
        pass

    def create_data(self):
        # TODO: to be continued
        try:
            job = {"Page": 0,
                   "Job_title": 0,
                   "Company": 0,
                   "Location": 0,
                   "Search_eng": 0,
                   "Term": 0,
                   "URL": 0,
                   "Words_of_concern": 0
                   }
            cmd = "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
            self.cursor.execute(cmd)
            return True

        except Exception as e:
            raise e

    def read_all_data(self, columns: "list of strings"):
        # TODO: to be continued
        try:
            cmd = "SELECT columns FROM table_name"
            self.cursor.execute(cmd)
            return True

        except Exception as e:
            raise e

    def update_data(self):
        # TODO: to be continued
        try:
            cmd = "UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;"
            self.cursor.execute(cmd)
            return True

        except Exception as e:
            raise e

    def delete_data(self):
        # TODO: Further development
        raise Exception('Not supported yet')


class Test():
    # TODO: to be continued
    def __init__(self):
        # instantiate
        db = JobDatabase.instantiate_Database()
        db.connect()
        print()


if __name__ == "__main__":
    Test()
