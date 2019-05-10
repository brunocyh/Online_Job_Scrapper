# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:38:55 2018

@author: Bruno
"""
"""
*********** server-side edition *************
How to maintain the app:
    - make sure it works properly: by checking whether every website works normally (tags, class...)
    - if mulfunction, send user message but run others normally
    - mulfunction defines as: returns []
"""

#from selenium import webdriver
import pandas as pd
import datetime
import time

class storageStructure(object):
    def __init__(self, stop_words):
        """
        Create data structure that holds all job information
        """
        self.datastructure = []
        self.length = 0
        self.stop_words = stop_words
    
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
    
    def return_len(self):
        return self.length
    
    def clear_stopwords(self, d):
        # O(n+c) operation        
        for i in self.stop_words:   
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
        self.length = len(df)
        
        if f_name != None: 
            df.to_csv(f_name, index = False)
        else:
            df.to_csv('job_dataset/Latest_Job_alert.csv', index = False)
        