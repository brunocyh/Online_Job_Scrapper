from lib.DatabaseService.JobDBService import JobDatabase
import random


def get_connected_db():
    db = JobDatabase.instantiate_Database()
    db.connect()
    return db


def test_instantiate():
    db = get_connected_db()
    assert db.disconnect()


def test_reset_table():
    db = get_connected_db()
    assert db.reset_table()


def test_sql():
    db = get_connected_db()
    iterator = db._sql("SELECT * FROM job_table")
    for item in iterator:
        print(item)
        return True

    assert False


def test_insert_item():
    db = get_connected_db()
    msg = db.create_data({
        "Page": "test",
        "Job_title": str(random.random()),
        "Company": str(random.random()),
        "Location": "test",
        "Search_eng": "test",
        "Term": "test",
        "URL": str(random.random()),
        "Words_of_concern": "test",
    })
    db.commit()
    assert msg


def test_read_data():
    db = get_connected_db()
    columns = ["Page", "Job_title"]
    assert type(db.read_all_data(columns).fetchall()) == list


def test_update_data():
    db = get_connected_db()
    conditions = ("Company", '0.018099086996902547')
    woc = ['citizen', 'junior', 'python']
    strified_woc = ','.join(woc)
    key_pair = ("Words_of_concern", strified_woc)
    assert db.update_analysed_data(conditions, key_pair)
