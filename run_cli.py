from lib.DatabaseService.JobDBService import JobDatabase
from CrawlingController import SearchEngine
from lib.DatabaseService.QueryController import Query


def reset_db(passcode):
    db = JobDatabase.instantiate_Database()
    db.connect()
    db.reset_table(passcode)
    return True


def explore_internet():
    terms = ['software engineering', 'backend development', 'full stack developer',
             'data analyst', 'data science']
    locations = ['brisbane']
    prefix = ['', 'parttime', 'junior']
    stop_words = ['senior', 'manager', 'director', 'postdoctoral', 'doctoral']
    words_of_concerns = []

    engine = SearchEngine(terms, locations, prefix,
                          stop_words, words_of_concerns)
    engine.execute()


def download_data():
    retriever = Query()
    columns = ["Job_title", "Company", "Location", "City", "Search_eng", "Term", "URL", "Words_of_concern", "created_time"]
    data = retriever.get_jobs_all(columns)
    data.sort_values("Company", inplace = True) 
    data.sort_values("created_time", inplace = True) 
    data.to_csv('job_details.csv', index=False)


if __name__ == "__main__":
    print('availble methods: set_up_database, explore_internet, download_data')
