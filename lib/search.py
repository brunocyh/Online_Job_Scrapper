# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:38:55 2018

@author: Bruno
"""
"""
*********** server-side edition *************
How to maintain this class:
    - make sure it works properly: by checking whether every website works normally (tags, class...)
    - if mulfunction, send user message but run others normally
    - mulfunction defines as: returns []
    
Polite Policy:
    - crawl delay applied (5-7 sec)
"""

#from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import lib.data_structure as d_structure
import re
import time
from random import randint

class Search(object):
    """
        This class handles the action of searching jobs on different jobboards. 
        And all the detailed implementations.
    """
    def __init__(self, search_terms, stop_words, location):
        
        self.search_terms = search_terms
        self.stop_words = stop_words
        self.location = location
        

    def brute_force_search(self):
        """
        This is the main programe of the scraper
        Job boards: Indeed, SEEK, Neuvoo
        In future: jora
        
        returns: a storage structure object
        """
        print('**Please be noted that this is a brute force search on multiple jobboards. I have applied crawler polite policy, make sure it is there to show some respects to web-owners. **')
        #n_terms = input('\n Please input more search terms? Format: ["developer","java engineer",...]: ')
        #search_terms.extend(n_terms)
        
        job_data = d_structure.storageStructure(self.stop_words)
        
        for term in self.search_terms:
            
            try:
                job_data.add_datas(self.crawl_indeed(term, self.location))
            except Exception as e:
                print('Error while searching {} with {}; {}'.format(term, 'Indeed', e))
                pass
            
            try:
                job_data.add_datas(self.crawl_SEEK(term, self.location))
            except Exception as e:
                print('Error while searching {} with {}; {}'.format(term, 'SEEK', e))
                pass
            
            try:
                job_data.add_datas(self.crawl_neuvoo(term, self.location))
            except Exception as e:
                print('Error while searching {} with {}; {}'.format(term, 'Neuvoo', e))
                pass
            
            try:
                job_data.add_datas(self.crawl_gumtree(term, self.location))
            except Exception as e:
                print('Error while searching {} with {}; {}'.format(term, 'Gumtree', e))
                pass
            
        # return to a data structure format, where it is sorted by post date
        return job_data
            
    
    def _parsingHTML(self,url):
        # html parsing
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, 'html.parser')
        return page_soup
    
    
    def crawl_indeed(self, term, location): ##
        #  Job: indeed        
        list_jobs = d_structure.storageStructure(self.stop_words)
        b_name = 'Indeed'
        print('Now searching {} from {} ...'.format(term, b_name))
        page = ['','&start=10','&start=20','&start=30','&start=40','&start=50','&start=60'] # say, 30 results for indeed
        for page, i in enumerate(page):
            
            # polite policy -- delay
            time.sleep(randint(5,8))            
            
            # url processing
            k_words = term.replace(" ", "-")
            domain = 'https://au.indeed.com/'
            url = 'jobs?q={}&l={}&sort=date' + i
            url = domain + url.format(k_words, location)
            
            # html parsing
            page_soup = self._parsingHTML(url)
        
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
    
    
    def crawl_SEEK(self, term, location): ##
        #  Job: seek
        # Policy: allows * crawlers for job search
        list_jobs = d_structure.storageStructure(self.stop_words)
        b_name = 'SEEK'
        print('Now searching {} from {} ...'.format(term, b_name))
        page = ['','&page=2', '&page=3', '&page=4','&page=5','&page=6','&page=7'] # say, 30 results for indeed
        for page, i in enumerate(page):
            
            # polite policy -- delay
            time.sleep(randint(5,8))              
            
            # url processing
            k_words = term.replace(" ", "-")
            domain = 'https://www.seek.com.au/'
            url = '{}-jobs/in-{}?sortmode=ListedDate' + i
            url = domain + url.format(k_words, location)
            
            # html parsing
            page_soup = self._parsingHTML(url)
        
            # find all job titles
            containers = page_soup.findAll("article")
            
            for job in containers:
                try:
                    # mapping
                    date = page ##
                    j_title = job['aria-label'] ##
                    company = job.find_all('a',{'data-automation':'jobCompany'})[0].text ##
                    loc = str(job(text=re.compile('area:')))[8:-2] ##                    
                    s_eng = b_name ##
                    term = term ##
                    u_link = domain + job.h1.a['href']
                    list_jobs.add_data(date, j_title, company, loc, s_eng, term, u_link)
                
                except:
                    list_jobs.add_data(99, 'error', 'error', 'error', s_eng, term, 'error')
        
            # Break if no result is returned from the first page
            if len(containers) == 0:
                if page == 0: print("No result returned from {}, with term {}".format(b_name, term))
                break
                
        return list_jobs.return_list()
    
    def crawl_neuvoo(self, term, location): ##
        #  Job: Neuvoo
        list_jobs = d_structure.storageStructure(self.stop_words)
        b_name = 'Neuvoo'
        print('Now searching {} from {} ...'.format(term, b_name))
        page = ['','2', '3', '4','5','6'] # say, 30 results for indeed
        for page, i in enumerate(page):
            
            # polite policy -- delay
            time.sleep(randint(5,8))      
            
            # url processing
            k_words = term.replace(" ", "+")
            domain = 'https://au.neuvoo.com'
            url = '/jobs/?k={}&l={}&f=&o=&p={}&r=15'
            url = domain + url.format(k_words, location, page)
            
            # html parsing
            page_soup = self._parsingHTML(url)
        
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
    
    def crawl_gumtree(self, term, location):
        #  Job: seek
        list_jobs = d_structure.storageStructure(self.stop_words)
        b_name = 'Gumtree'
        print('Now searching {} from {} ...'.format(term, b_name))
        page = ['','page-2/', 'page-3/','page-4/','page-5/'] # say, 30 results for indeed
        for page, i in enumerate(page):
            
            # polite policy -- delay
            time.sleep(randint(5,8))  
            
            # url processing
            k_words = term.replace(" ", "-")
            domain = 'https://www.gumtree.com.au'
            url = '/s-jobs/{}/{}/{}k0c9302l3005721?sort=rank&ad=offering'
            url = domain + url.format(location, k_words, page)
            
            # html parsing
            page_soup = self._parsingHTML(url)
        
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