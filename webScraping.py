# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:38:55 2018

@author: Bruno
"""
"""
How to maintain the app:
    - make sure it works properly: by checking whether every website works normally (tags, class...)
    - if mulfunction, send user message but run others normally
    - mulfunction defines as: returns []
"""

from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import re
import datetime
import time
global stop_words 

def brute_force_search(search_terms, location):
    """
    This is the main programe of the scraper
    Job boards: Indeed, SEEK, Neuvoo
    In future: jora, 
    """
    print('**Please be noted that this is a brute force search on multiple jobboards (which is not very welcomed by most website. I built it for personal usage only so I will bear NO legal liability k?). Bruno**')
    #n_terms = input('\n Please input more search terms? Format: ["developer","java engineer",...]: ')
    #search_terms.extend(n_terms)
    
    
    job_data = storageStructure()
    
    for term in search_terms:
        
        try:
            job_data.add_datas(crawl_indeed(term,location))
        except:
            print('Error while searching {} with {}'.format(term, 'Indeed'))
            pass
        
        try:
            job_data.add_datas(crawl_SEEK(term,location))
        except:
            print('Error while searching {} with {}'.format(term, 'SEEK'))
            pass
        
        try:
            job_data.add_datas(crawl_neuvoo(term,location))
        except:
            print('Error while searching {} with {}'.format(term, 'Neuvoo'))
            pass
        
        try:
            job_data.add_datas(crawl_gumtree(term,location))
        except:
            print('Error while searching {} with {}'.format(term, 'Neuvoo'))
            pass
        
        #job_data.add_datas(crawl_linkedIn(term,location)) #required login
        
    # return to a data structure format, where it is sorted by post date
    return job_data
        

def _parsingHTML(url):
    # html parsing
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')
    return page_soup


def crawl_indeed(term, location): ##
    #  Job: indeed
    list_jobs = storageStructure()
    b_name = 'Indeed'
    print('Now searching {} from {} ...'.format(term, b_name))
    page = ['','&start=10','&start=20','&start=30','&start=40','&start=50','&start=60'] # say, 30 results for indeed
    for page, i in enumerate(page):
        
        # url processing
        k_words = term.replace(" ", "-")
        domain = 'https://au.indeed.com/'
        url = 'jobs?q={}&l={}&sort=date' + i
        url = domain + url.format(k_words, location)
        
        # html parsing
        page_soup = _parsingHTML(url)
    
        # find all job titles
        containers = page_soup.findAll("div", {"data-tn-component":"organicJob"})
        for job in containers:
            
            try:
                # mapping
                date = page ##
                j_title = job.h2.text.strip()
                company = job.findAll("span",{'class':'company'})[0].text.strip()
                loc = job.findAll("span",{'class':'location'})[0].text.strip()
                s_eng = b_name ##
                term = term ##
                u_link = domain + job.h2.a['href'].strip()
                list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
                
            except:
                list_jobs.add_data(99, 'error', 'error', 'error', s_eng, term, 'error')
            
    # Break if no result is returned from the first page
        if len(containers) == 0:
            if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
            break
            
    return list_jobs.return_list()


def crawl_SEEK(term, location): ##
    #  Job: seek
    list_jobs = storageStructure()
    b_name = 'SEEK'
    print('Now searching {} from {} ...'.format(term, b_name))
    page = ['','&page=2', '&page=3', '&page=4','&page=5','&page=6','&page=7'] # say, 30 results for indeed
    for page, i in enumerate(page):
        
        # url processing
        k_words = term.replace(" ", "-")
        domain = 'https://www.seek.com.au/'
        url = '{}-jobs/in-{}?sortmode=ListedDate' + i
        url = domain + url.format(k_words, location)
        
        # html parsing
        page_soup = _parsingHTML(url)
    
        # find all job titles
        containers = page_soup.findAll("article")
        for job in containers:
            
            # mapping
            date = page ##
            j_title = job['aria-label'] ##
            company = job.find_all('a',{'data-automation':'jobCompany'})[0].text ##
            loc = str(job(text=re.compile('area:')))[8:-2] ##
            s_eng = b_name ##
            term = term ##
            u_link = domain + job.h1.a['href']
            list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
    
        # Break if no result is returned from the first page
        if len(containers) == 0:
            if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
            break
            
    return list_jobs.return_list()

def crawl_neuvoo(term, location): ##
    #  Job: Neuvoo
    list_jobs = storageStructure()
    b_name = 'Neuvoo'
    print('Now searching {} from {} ...'.format(term, b_name))
    page = ['','2', '3', '4','5','6'] # say, 30 results for indeed
    for page, i in enumerate(page):
        
        # url processing
        k_words = term.replace(" ", "+")
        domain = 'https://au.neuvoo.com'
        url = '/jobs/?k={}&l={}&f=&o=&p={}&r=15'
        url = domain + url.format(k_words, location, page)
        
        # html parsing
        page_soup = _parsingHTML(url)
    
        # find all job titles
        containers = page_soup.findAll("div",{'class':'job-c'})
        for job in containers:
            
            # mapping
            date = page ##
            j_title = job.h2.text.strip() ##
            company = job.find_all('span',{'class':'j-empname-label'})[0].text ##
            loc = job.find_all('div',{'class':'j-location'})[0].span.text ##
            s_eng = b_name ##
            term = term ##
            u_link = domain + job.h2.a['href']
            list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
    
        # Break if no result is returned from the first page
        if len(containers) == 0:
            if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
            break
            
    return list_jobs.return_list()

def crawl_gumtree(term, location):
    #  Job: seek
    list_jobs = storageStructure()
    b_name = 'Gumtree'
    print('Now searching {} from {} ...'.format(term, b_name))
    page = ['','page-2/', 'page-3/','page-4/','page-5/'] # say, 30 results for indeed
    for page, i in enumerate(page):
        
        # url processing
        k_words = term.replace(" ", "-")
        domain = 'https://www.gumtree.com.au'
        url = '/s-jobs/{}/{}/{}k0c9302l3005721?sort=rank&ad=offering'
        url = domain + url.format(location, k_words, page)
        
        # html parsing
        page_soup = _parsingHTML(url)
    
        # find all job titles
        containers = page_soup.findAll('a',{'class':'user-ad-row user-ad-row--no-image link link--base-color-inherit link--hover-color-none link--no-underline'})
        for job in containers:
            
            # mapping
            date = page ##
            details = job['aria-label'].split('.')
            j_title = details[0] ##
            company = "n/a"
            loc = details[2].strip().strip('\n Location: ') ##
            s_eng = b_name ##
            term = term ##
            u_link = domain + job['href']
            list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
    
        # Break if no result is returned from the first page
        if len(containers) == 0:
            if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
            break
            
    return list_jobs.return_list()

def crawl_linkedIn(term, location):
    #  Job: LinkedIn... But required logging in; This is risky
    list_jobs = storageStructure()
    b_name = 'LinkedIn'
    print('Now searching {} from {} ...'.format(term, b_name))
    page = ['','&start=25', '&start=50', '&start=75'] 
    browser = webdriver.Chrome()
    
    for page, i in enumerate(page):
        # url processing
        k_words = term.replace(" ", "%20")
        domain = 'https://www.linkedin.com'
        url = '/jobs/search/?country=au&countryCode=au&keywords={}&location={}%2C%20Australia&locationId=au%3A4909&sortBy=DD' + i
        url = domain + url.format(k_words, location)
        
        # avoid linkedIn block / parse html
        browser.get(url)
        page_soup = soup(browser.page_source, 'html.parser')
        browser.quit()        
    
        # find all job titles
        containers = page_soup.findAll("div",{'class':'job-details'})
        
        for job in containers:
            
            # mapping
            date = page ##
            j_title = job.h2.text ##
            company = job.find_all('div',{'class':'company-name'})[0].text 
            loc = 'na'
            s_eng = b_name ##
            term = term ##
            u_link = domain + job.h2.a['href'] ##
            list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
    
        # Break if no result is returned from the first page
        if len(containers) == 0:
            if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
            break
            
    return list_jobs.return_list()


class storageStructure(object):
    def __init__(self):
        """
        Create data structure that holds all job information
        """
        self.datastructure = []
    
    def add_data(self, date, j_title, company, location, s_eng, term, url):
        """
        Temp data structure ==> [[date, j,c,l,s,t],
                                 [date, j,c,l,s,t],
                                 [date, j,c,l,s,t]...]
        """
        entry = [date, j_title, company, location, s_eng, term, url]
        self.datastructure.append(entry)
        
    def add_datas(self, list_crawled_results):
        self.datastructure.extend(list_crawled_results)
        
    
    def return_list(self):
        return self.datastructure
    
    def clear_stopwords(self, d):
        # O(n+c) operation        
        for i in stop_words:   
            d = d[~d['Job_title'].str.contains(i, case= False)]
            
        return d
    
    def clear_duplicates(self, df):
        # O(n^2) operation
        df_new = []
        com_roles = []
        last_com = ""
        df = df.sort_values('Company', ascending=True)
        
        for n, com in enumerate(df['Company']):
            this_job = df.iloc[n]['Job_title']
            if com == last_com:
                if this_job in com_roles:
                    # same role.. do not book in
                    pass
                else:
                    # same company but not recorded
                    df_new.append(df.iloc[n].values)
                    com_roles.append(this_job)
                    
            else:
                # this row is new company vs last --> record it down
                com_roles = []
                df_new.append(df.iloc[n].values)            
                com_roles.append(this_job)
                
            last_com = com
                
        return pd.DataFrame(df_new, columns=['Page','Job_title','Company','Location','Search_eng','Term', 'URL'])
    
    def export_csv(self, f_name = None):
        """
        - to dataframe
        - sort date
        - stop word elimination
        - clear duplicates
        - output to csv
        """
        print('Exporting Data...')
        df = pd.DataFrame(self.datastructure, columns=['Page','Job_title','Company','Location','Search_eng','Term', 'URL'])
        df = self.clear_stopwords(df) # clear stop words        
        df = self.clear_duplicates(df) # clear job duplicates
        
        if f_name != None: 
            df.to_csv(f_name, index = False)
        else:
            df.to_csv('job_dataset/Latest_Job_alert.csv', index = False)
        

#### RUN programe
if __name__ == "__main__":    

    # ----- Customize Parameters -----\
    #search_terms = ['part time','data entry','barista','junior'] ## casual
    search_terms = ['software engineering', 'internship developer', 'data science', 'programmer', 'developer','python','graduate developer', 'part time developer','junior developer','data analyst']
    
    locations = ['brisbane']
    stop_words = ['senior','manager','director','postdoctoral','doctoral','experienced']
    concern_key_words = ['citizen', 'pr', 'permanent', 'resident', 'years', 'experienced', 'ethic', 'stress', 'multinational','visa','right','must','only','lead','mentor', 'python']
    
    print('----------------- INFO -------------------')
    print('Locations: {}'.format(locations))
    print('Stop words: {}'.format(stop_words))
    input('You are searching for {}, continue...'.format(search_terms))
    
    # ----- End customizing -----
    for loc in locations:
        # 1. Job crawling...
        print('Crawling jobs from ' + loc)
        result = storageStructure()
        result = brute_force_search(search_terms, loc)
        tstmp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H_%M')
        f_name = '{}_jobs{}'.format(loc, tstmp)
        result.export_csv('job_dataset/{}.csv'.format(f_name))
        
    j_count = len(result)
    print("{} jobs are found".format(j_count))
    res = input("Job search completed!! Do you wish to analyse job discription? Press 'N' to exit (any to continue)... ")
    if res == 'N' or res == 'n':
        exit()
    
    # 2. Content analysing...
    import lib.contentAnalysing as ca
    print('Begin crawling job details in {}'.format(loc))
    result2 = ca.crawler(concern_key_words, 'job_dataset/{}.csv'.format(f_name))
    
    try: 
        result2.crawl_content(j_count)
        result2.export_csv('job_dataset/{}_analysed.csv'.format(f_name))    
        
    except Exception as e:
        input(e)
        exit()
        
    input("Job hunt done, go chase your dream!!")
        