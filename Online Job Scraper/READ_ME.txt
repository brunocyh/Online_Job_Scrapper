---- Disclaimer!! ----
This algorithm is violent in nature, it is definietly not for commercial use and it is not build for that 
purpose. It is build for personal / educational usage only by Bruno. The author will NOT be responsible for
any losses / legal issues involved in the use of it. 
@Copyright retained by Bruno Cheung, 2018

---- What is it? ----
So this is a web crawler that crawls through the mainstream jobboards in Australia. Eh.. so why do I want to spend my entire weekend building this thing? I have a few problems faced when I started looking jobs online...

The Problem I faced: 
- I have to look for jobboard one by one
- I have multiple search terms which return me with different job sugegstions (eg python developer, data scientist)
- I want to skip through annoying job titles like manager / senior (I am a fresh grad!)
- Jobboards normally returns 10 - 15 jobs in a time 
- I am concerned about the job details (content), some say aussie citizenship is required.. some say 5 years of experience
- oh.. how is the job opportunity in sydney and melbourn..?
- Yes, it is just way too TIME CONSUMING and tedious and boring! But this is how we normally job hunt!

My Solution:
- this crawler lists out all the jobs available gathered from the first few pages in mainstream jobboards in no time
- I can also search multiple terms at once
- duplicates that returned from different jobboards/search terms will be elminate
- all jobs are export to structured csv file
- job descriptions of each jobs returned are then evaluated. Will outline the keywords I am looking for from each job's description
- All the problems listed above are solved! 

I am a data scientist thus I enjoy traversing jobs (to me, data of interest) in excel instead of browser.. I can even filter out jobs that does not interest me (or only to those interest me). It is designed to run completely automatic, thus, I can run the script in every day at 5am on cloud. Then start writing my cover letter for my favourite jobs in the morning.


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