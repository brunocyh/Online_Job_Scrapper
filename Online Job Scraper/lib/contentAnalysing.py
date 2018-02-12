# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 16:42:44 2018

@author: Bruno
"""
import pandas as pd
from nltk.stem.snowball import SnowballStemmer as stemmer
from nltk import word_tokenize
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import chardet

class crawler(object):
    def __init__(self, key_words, f_name):
        self.key_words = self._stem(key_words) # requires lower + stemming
        self.f_name = f_name
        
        # detect encoding method:
        with open(f_name, 'rb') as f:
            r = chardet.detect(f.read())  # or readline if the file is large
            
        self.df = pd.read_csv(f_name, encoding=r['encoding'])
        self.df['Words_of_concern'] = ''
    
    def crawl_content(self):
        """
        - traverse DF
        - detect which jobboard
        - crawl job description (url) ==> tokenize ==> lower ==> stemming
        - for those keywords appear in each job, list them out in extra column
        - next job
        """
        for i, row in self.df.iterrows():
            print('Analysing ' + str(row.Job_title) + ' at ' + str(row.Company) + ' -- Job number:'+ str(i))            
            
            # html crawling
            url = row.URL
            engine = row.Search_eng
            w_bag = self._auto_crawl(engine, url)
            
            if w_bag != 'Error occured':
                w_bag = word_tokenize(w_bag)
                
                # word processing
                w_bag = self._stem(w_bag)
                exist_kwords = self._find_kwords(w_bag)
            else:
                woc = "*Error scrapping"
            
            # modify df
            woc = exist_kwords.strip(" &")
            if woc == "": woc = '*No found'            
            self.df.at[i,"Words_of_concern"] = woc
    
    def export_csv(self, f_name):
        self.df.to_csv(f_name, index=False)
        
    def _stem(self, b_words):
        """
        Takes in a list of words, it will lower and stem it
        return list of stemmed words
        """
        st = stemmer("english")
        return [st.stem(word) for word in b_words]
    
    def _find_kwords(self, b_words):
        """
        Given a bag of words, it tried to identify all the keywords given
        return the keywords that exist in the content
        """
        k_words = ""
        for kw in self.key_words:
            
            #input(kw)
            if kw in b_words:
                #input("ya, its in b_words")   
                # extend the str
                k_words = kw + " & " + k_words
        
        return k_words
        
    def _auto_crawl(self, engine, url):
        """
        Determine which crawler to use & process
        return List of words (content)
        """
        b_words = ""
        
        try: 
            # select the appropriate crawler
            if engine == "SEEK":
                b_words = self._analyse_SEEK(url)
            elif engine == "Indeed":
                b_words = self._analyse_Indeed(url)
            elif engine == "Neuvoo":
                b_words = self._analyse_Neuvoo(url)
            elif engine == "Gumtree":
                b_words = ""
            else:
                b_words = self._analyse_General(url)
                
        
        except:
            b_words = 'Error occured'
            print("Error parsing html" + " with " + engine + " at " + url)
        
        return b_words
        
    def _analyse_SEEK(self, url): ##
        page_soup = self._parsingHTML(url)
        container = page_soup.find('div',{'class':'templatetext'})  
        
        if container == None:
            # non-jobboard parsing
            details = self._analyse_General(url, page_soup)
            
        else:
            # Normal parsing
            details = ""
            for con in container.findChildren():
                txt = con.text
                details = details + " " + txt
            
        return details
    
    def _analyse_Indeed(self, url): ##
        page_soup = self._parsingHTML(url)
        container = page_soup.find('td',{'class':'snip'})
        
        if container == None:
            # non-jobboard parsing
            details = self._analyse_General(url, page_soup)
            
        else:
            # Normal parsing
            details = ""
            for con in container.findChildren():
                txt = con.text
                details = details + " " + txt
            
        return details
    
    def _analyse_Neuvoo(self, url): ##
        page_soup = self._parsingHTML(url)
        container = page_soup.find('div',{'class':'view-job-description'})
        
        if container == None:
            # non-jobboard parsing
            details = self._analyse_General(url, page_soup)
            
        else:
            # Normal parsing
            details = ""
            for con in container.findChildren():
                txt = con.text
                details = details + " " + txt
            
        return details
    
    def _analyse_Gumtree(self, url): # Not used, since url incorrect
        page_soup = self._parsingHTML(url)        
        container = page_soup.find('div',{'class':'job-description'})        
        
        if container == None:
            # non-jobboard parsing
            details = self._analyse_General(url, page_soup)
            
        else:
            # Normal parsing
            details = ""
            for con in container.findChildren():
                txt = con.text
                details = details + " " + txt
            
        return details
    
    def _analyse_General(self, url, page_soup = None):
        """
        Special case: if failed to capture --> 
        pass in html parse and conduct general parse
        """
        if page_soup == None:
            # come in normal
            page_soup = self._parsingHTML(url)
        else:
            # come in while failed
            pass
            
        container = page_soup.find('body')        
        details = ""
        for con in container.findChildren():
            txt = con.text
            details = details + " " + txt
            
        return details
    
    def _parsingHTML(self, url):
        """
        html parsing
        """
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, 'html.parser')
        return page_soup
        

if __name__ == "__main__":
    # used only when jobs are found
    f_name = input("Please enter the name of the job file: ")    
    #f_name = "../job_dataset/brisbane_jobs_testing.csv"
    k_words = ['citizen', 'pr', 'permanent', 'resident', 'years', 'experienced', 'cover letter', 'ethic', 'stress', 'multinational','visa','right','must','only']
    result2 = crawler(k_words, f_name)
    result2.crawl_content()
    result2.export_csv('../job_dataset/{}_analysed.csv'.format(f_name))
    input("Analysing completed! Press anything to exit...")