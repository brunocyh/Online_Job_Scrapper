from lib.DatabaseService.JobDBService import JobDatabase
from lib.OperationsController.CrawlingController import SearchEngine


def set_up_database(passcode):
    db = JobDatabase.instantiate_Database()
    db.connect()
    db.reset_table(passcode)
    return True


def explore_internet():
    terms = ['software engineering', 'backend development', 'full stack developer',
             'data analyst', 'data science']
    locations = ['brisbane']
    prefix = ['parttime', 'junior']
    stop_words = ['senior', 'manager', 'director', 'postdoctoral', 'doctoral']
    words_of_concerns = []

    engine = SearchEngine(terms, locations, prefix,
                          stop_words, words_of_concerns)
    engine.execute()


def download_data():
    print('not yet')
    pass


if __name__ == "__main__":
    print('availble methods: set_up_database, explore_internet, download_data')
