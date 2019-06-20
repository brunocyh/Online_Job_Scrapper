from lib.OperationsController.CrawlingController import SearchEngine

if __name__ == "__main__":
    if input('Press Y to continue... ') == 'Y':
        engine = SearchEngine(term= 'software engineer', location="Brisbane")
        engine.execute()
    
    else:
        print('bye')