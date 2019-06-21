from lib.OperationsController.CrawlingController import SearchEngine
from run_cli import run_crawl

if __name__ == "__main__":
    if input('Press Y to continue... ') == 'Y':
        run_crawl()
    
    else:
        print('bye')