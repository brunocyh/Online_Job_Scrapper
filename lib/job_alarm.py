# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:25:58 2018

@author: Administrator
"""
import pandas as pd
import os
import datetime
import time
import chardet

class Alarm(object):
    def __init__(self):
        self.dataset = pd.DataFrame()
    
    def find_yesterday(self, folder_dir, more = None): #DONE
        """
        Input: Job dataset directory
        Return the name of the FIRST file created ytd (or last ava date)
        """
        l = os.listdir(folder_dir)
        
        # get all csv files then sort them according to their datetime
        s = []
        for i in l:
            if "_analysed.csv" in i:
                s.append(i)
                
        s.sort()
        
        if more == None:
            # get latest non-today
            c = -1
            today = datetime.datetime.fromtimestamp(time.time())
            id_index = s[c].find("@")
            
            f_date = s[c][id_index-10:id_index]
            #f_date_obj = datetime.strptime(f_date, '%Y-%m-%d')
            #f_date = (today-datetime.timedelta(days=day)).strftime('%Y-%m-%d')
            today = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
            next_f_date = f_date
            
            # - more days (3 days also consider new roles)
            while today <= (f_date) or (f_date) == next_f_date:
                c-=1
                f_date = s[c][id_index-10:id_index]
                next_f_date = s[c-1][id_index-10:id_index]    
                
            retn = s[c]
        else:
            retn = s[3]
        
        return retn
    
    def find_new_jobs(self, lastest_fname, ytd_file_fname): #tbt
        """
        Complexity: (nLogn + n) ie nLogn Instead of n^2
        Input: filenames
        Return void; but store DataFrame internally
        """
        print("Discovering new roles...")
        # detect encoding method:
        with open(lastest_fname, 'rb') as f:
            r = chardet.detect(f.read())  # or readline if the file is large
        my_file = pd.read_csv(lastest_fname, encoding=r['encoding'])
        my_file['New_job'] = ""
        
        with open(ytd_file_fname, 'rb') as f:
            r = chardet.detect(f.read())  # or readline if the file is large
        y_file = pd.read_csv(ytd_file_fname, encoding=r['encoding'])
        
        
        # sort both files (n log n)
        my_file = my_file.sort_values('Company', ascending=True)
        y_file = y_file.sort_values('Company', ascending=True)
        
        # traverse both file... only once each (n)        
        my_index = 0
        y_index = 0
        my_index_max = len(my_file)
        y_index_max = len(y_file)
        
        while (my_index +1) < my_index_max and (y_index+1) < y_index_max:
            my_current = my_file.iloc[my_index]['Company']
            y_current = y_file.iloc[y_index]['Company']
            
            if my_current < y_current:
                # Non-exist companies --> simply label as new
                my_file.at[my_index,"New_job"] = "*new!"
                my_index += 1
            
            elif my_current > y_current:
                # Need to catch up with my until y > or == to my
                y_index += 1
                
            elif my_current == y_current:
                # Same company --> interesting
                y_jobs = []
                this_company = y_current
                
                # record all the index == same company
                while y_current == this_company:
                    y_jobs.append(y_file.iloc[y_index]['Job_title'])   
                    
                    # update for while loop
                    if (y_index +1) >= y_index_max:
                        break
                    
                    y_index += 1
                    y_current = y_file.iloc[y_index]['Company']
                    
                    
                    
                # check whether my_current.samecompany "in" y_list
                while my_current == this_company:   
                    my_current_job = my_file.iloc[my_index]['Job_title']
                    
                    if my_current_job not in y_jobs: 
                        my_file.at[my_index,"New_job"] = "*new role!"
                        
                    else:
                        # Duplicates
                        pass
                    
                    # update for while loop
                    if (my_index +1) >= my_index_max:
                        break
                    
                    my_index += 1
                    my_current = my_file.iloc[my_index]['Company']
                    
        self.dataset = my_file
    
    def rewrite(self, filename):
        """
        Input: filenames
        Return void; but rewrite the file 
        """
        self.dataset.to_csv(filename, index = False)