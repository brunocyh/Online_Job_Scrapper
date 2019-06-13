from lib.DatabaseService.JobDBService import JobDatabase
import pytest


def get_connected_db():
    db = JobDatabase.instantiate_Database()
    db.connect()
    return db


def test_instantiate():
    db = get_connected_db()
    db.disconnect()
    print('hello')


def test_reset_table():
    db = get_connected_db()
    db.reset_table()


def test_sql():
    db = get_connected_db()
    iterator = db._sql("SELECT * FROM job_table")

    for item in iterator:
        print(item)

    assert False


@pytest.mark.focus
def test_insert_item():
    pass
