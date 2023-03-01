from DatabaseService.LocalSQLDatabase import JobDatabase
import random
from DataModels import JobBuilder, JobModel


def get_connected_db():
    db = JobDatabase.instantiate_Database()
    db.connect()
    return db


def test_instantiate():
    db = get_connected_db()
    assert db.disconnect()


def test_reset_table():
    db = get_connected_db()
    assert db.reset_table(passcode='4321')


def test_sql():
    db = get_connected_db()
    iterator = db._sql("SELECT * FROM job_table")
    for item in iterator:
        return True

    assert False


def test_insert_item():
    db = get_connected_db()
    builder = JobBuilder()
    builder.set_company(str(random.random()))
    builder.set_jobtitle(str(random.random()))
    builder.set_location(str(random.random()))
    builder.set_page(str(random.random()))
    builder.set_search_engine('test engine')
    builder.set_term(str(random.random()))
    builder.set_url(str(random.random()))
    builder.set_word_of_concerns(str(random.random()))
    msg = db.create_data(builder.build())
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

# def test_contains():
#     db = get_connected_db()
#     assert print(db.contains('404'))
    