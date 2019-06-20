from lib.DatabaseService.JobDBService import JobDatabase


def set_up_database(passcode):
    db = JobDatabase.instantiate_Database()
    db.connect()
    db.reset_table(passcode)
    return True

if __name__ == "__main__":
    set_up_database(input('Reset password: '))