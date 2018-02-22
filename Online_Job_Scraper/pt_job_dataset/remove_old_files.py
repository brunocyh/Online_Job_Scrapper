# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:57:24 2018

@author: Administrator

Schedule to run every 12am
"""
import os


if __name__ == '__main__':
    # list out all files
    data_dir = "C:/Users/Administrator/Desktop/Online_Job_Scraper/job_dataset"
    files = os.listdir(data_dir)
    files.sort()
    files.remove("remove_old_files.py")    
    
    # survive files
    lim = 30
    if len(files) >= lim:
        # spare
        spare = len(files) - lim
        d_files = files[0:spare]
        
        # del
        for f in d_files:
            os.remove(f)
    
    
    