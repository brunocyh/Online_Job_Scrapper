# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:25:58 2018

@author: Administrator
"""
# import 3rd parties
import os
import datetime
import time

#### RUN programe
if __name__ == "__main__":    
    
    # --------------------------------
    # ----- Customize Parameters -----
    cdir = "Online_Job_Scraper"
    os.chdir(cdir)
    pri = ['','parttime ','graduate ','junior ','internship ']
    search_term = ['software engineering', 'data science', 'developer','data analyst','python', 'business analytics', 'business intelligence']
    
    # .. combine all key-words to form a list of search terms
    search_terms = []
    for p in pri:
        for s in search_term:
            w = p + s
            search_terms.append(w)
            
    locations = ['brisbane']
    stop_words = ['senior','manager','director','postdoctoral','doctoral']
    concern_key_words = ['citizen', 'citizenship', 'permanent', 'resident', 'years', 'experience', 'ethic', 'senior', 'multinational','require','must','graduate','minimum','mentor', 'python','java','.net','c#']                     
    # ----- End customizing -----
    # --------------------------------
    # import my lib
    
    import lib.search as search
    import lib.contentAnalysing as ca
    
    print('----------------- INFO -------------------')
    print('Locations: {}'.format(locations))
    print('Stop words: {}'.format(stop_words))
    print('You are searching for {}, continue...'.format(search_terms))
    print('----------------- INFO -------------------')
    
    loc = locations[0]
    # 1. Job crawling...
    print('Crawling jobs from ' + loc)
    
    
    # create object
    search_obj = search.Search(search_terms, stop_words, loc)
    result = search_obj.brute_force_search()
    
    try:
        tstmp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H_%M')
        f_name = '{}_jobs{}'.format(loc, tstmp)
        result.export_csv('{}/job_dataset/{}.csv'.format(cdir, f_name))
            
        j_count = result.return_len()
        print("{} jobs are found".format(j_count))
    
    except Exception as e:
        input(e)
        exit()

    
    # 2. Content analysing...
    print('Begin crawling job details in {}'.format(loc))
    result2 = ca.crawler(concern_key_words, '{}/job_dataset/{}.csv'.format(cdir, f_name))
    
    try: 
        result2.crawl_content(j_count)
        result2.export_csv('{}/job_dataset/{}_analysed.csv'.format(cdir, f_name))    
        
    except Exception as e:
        input(e)
        exit()
    
    # 3. Update alarms: (adding alarm columns to existing sheet)
    import lib.job_alarm as j_alarm
    alarm = j_alarm.Alarm()
    
    try:
        ytd_name = alarm.find_yesterday("{}/job_dataset".format(cdir), more = 1)
        ytd_name = '{}/job_dataset/{}'.format(cdir, ytd_name)
        newest_file = '{}/job_dataset/{}_analysed.csv'.format(cdir, f_name)
        alarm.find_new_jobs(newest_file, ytd_name)
        alarm.rewrite(newest_file)
    
    except Exception as e:
        print(e)
        input("In order to use new job alert function, please obtain at least 2 days of analysed datasets")

    print("done!")
    exit()