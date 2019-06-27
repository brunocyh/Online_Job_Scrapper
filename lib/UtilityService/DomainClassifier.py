from enum import Enum

class Jobboards(Enum):
    gumtree = "gumtree.com"
    indeed = "indeed.com"
    neuvoo = "neuvoo.com"
    seek = "seek.com"
    universal = "universal"

class Classifier():
    current_job_boards = []
    
    def identify_jobboard(self, url):
        pass