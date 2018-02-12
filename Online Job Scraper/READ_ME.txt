---- Disclaimer!! ----
This algorithm is violent in nature, it is definietly not for commercial use and it is not build for that 
purpose. It is build for personal / educational usage only by Bruno. The author will NOT be responsible for
any losses / legal issues involved in the use of it. 
@Copyright retained by Bruno Cheung, 2018

---- Files and folders: ----
## webScrapping.py: main program that scrap though all the jobs (search through SEEK, Indeed, Gumtree, Neuvoo)
## job_dataset: a folder contains all job datasets
#### XXXX_recent_jobs.csv: dataset generated after webScrapping (XXXX == name of city)
#### XXXX_analysed_jobs.csv: dataset generated after job desciptions were analysed (XXXX == name of city)
## lib: a folder contains extra-functions
#### contentAnalysing.py: content scraping, identifying the keywords job seekers concerns about in job description

---- About && External Libraries used: ----
Name: Online Job Scraper v2.3.0
Python version: 3.6
pandas
beautifulsoap4
nltk
selenium