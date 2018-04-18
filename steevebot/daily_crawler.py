import requests
import re
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
# from billiard import Pool
import time

import traceback
# import concurrent.futures
# from itertools import repeat

from .tor_session import *

from .models import Job

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def retry_write_into_dict(input_data):
    href = []
    renewTorIP()
    try:
        print("debug retry write into dict:", 1)
        with Pool(processes=70) as pool:
            href += pool.map(write_into_dict, input_data) 
        print("debug retry write into dict:", 2)
    except:
        print("debug retry write into dict:", 3)
        print()
        traceback.print_exc()
        print()
        href = []
    return href

def retry_fetch_article_content(href):
    contents = []
    renewTorIP()
    try:
        with Pool(processes=70) as pool:
            contents += pool.map(fetch_article_content, href)
    except:
        print()
        traceback.print_exc()
        print()
        contents = []
    return contents

def daily_updater(Key_work):
    print("debug:", 0)
    
    renewTorIP()
    print("debug:", 1)
    start = time.time()
    
    domain_name = 'https://www.dice.com'

    ## Input you want
    Key_location =''
    key_main=domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-1-jobs?'

    ## Calculate Job Pages
    response_main = session.get(key_main)
    soup = BeautifulSoup(response_main.text,'lxml')
    try:
        pages = int(str(soup.find("",{"id":"posiCountId"}).text).replace(',',''))//30
    except:
        print("Load Pages Error. Stop Updating", Key_work)
        return
    print('Total have ' + str(pages) + ' pages')

    print("debug:", 2)
    input_data = [ (page, domain_name, Key_work, Key_location) for page in range(1, pages+1) ]
    
    href = retry_write_into_dict(input_data)
    cc = 1
    while not href:
        href = retry_write_into_dict(input_data)
        cc += 1
        print("debug cc:", cc)
#     print(cc)
    
    print("debug:", 3)

    href = [ url for page_href in href for url in page_href ]
    print("Total have : " + str(len(href)))

    contents = retry_fetch_article_content(href)
    cc = 1
    while not contents:
        contents = retry_fetch_article_content(href)
        cc += 1
    print(cc)

    print("debug:", 4)
    
    renewTorIP()

    result = load_to_json(Key_work, contents)
    print(len(result[Key_work]))

    create_data(Key_work, result)
    
    end = time.time()
    print("\nDone with " + Key_work + " >>  " + str(end-start) + " sec")
    
    # return result
    

## Add all pages's work
def write_into_dict(input_data):
    page, domain_name, Key_work, Key_location = input_data[0], input_data[1], input_data[2], input_data[3]
    try:
        response_page = session.get(domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-'+str(page)+'-jobs?', headers=headers)
    except:
        print('Write into dict Error!!')
        raise

    soup1 = BeautifulSoup(response_page.text,'lxml')
    # every page contains 30 urls
    page_href = []
    for i in range(30):
        try:
            tmp = domain_name + soup1.find("",{"id":"position"+str(i)}).get('href')
            page_href.append(requests.utils.requote_uri(tmp))
        except:
            print()
            traceback.print_exc()
            print()

    if page%30 == 0:
        print('page '+ str(page)+' is finished')
        
    return page_href

def fetch_article_content(url):
    judege  = True
    try:
        response_work = session.get(url, headers=headers)
    except:
        print()
        traceback.print_exc()
        print()
        raise

    soup = BeautifulSoup(response_work.text,'lxml')
    if soup.find("",{"class":"pull-left h1 jobs-page-header-h1"}):
        judege = False
    if soup.find("",{"class":"col-md-12 error-page-header"}):
        judege = False
    
    
    if judege==True:
        try:
            
            jobTitle = soup.find("",{"class":"jobTitle"}).text
            
            jobEmployer = soup.find("",{"class":"employer"}).text.replace('\n','').replace('\t','')
            jobLocation = soup.find("",{"class":"location"}).text.replace('\n','')
            jobPostTime = soup.find("",{"class":"posted hidden-xs"}).text
            jobID = soup.find("",{"class":"company-header-info"}).text
            jobID = jobID.replace('\n','').split(':')[2].strip().replace('-','')
            ## tag job-info is a array .
            foo = soup.find_all("",{"class":"row job-info"})

            out = []
            for o in foo:
                out.append(o.text.replace('\n','').replace('\t',''))

        except:
            out = []
            jobTitle='None'
            jobEmployer='None'
            jobLocation='None'
            jobPostTime='None'
            foo='None'
            jobID='None'
            #jobDescription=''   

        try:
            jobskillss = out[0]
            jobemploymentType = out[1]
            jobbaseSalary = out[2]

        except IndexError:
            jobskillss = 'None'
            jobemploymentType = 'None'
            jobbaseSalary = 'None'

    ## Jobdescription
        str1 = str(soup.find("",{"id":"jobdescSec"}))
        soup = BeautifulSoup(str1.replace('<br/>','\n').replace('</li>','\n').replace('</strong>','\n').replace('</p>','\n').replace('<p>','\n'),'lxml')
        jobDescription = soup.text
        joburl = url
    else:
        return
        
    
    return((jobTitle,jobEmployer,jobLocation,jobPostTime,jobID,jobskillss,jobemploymentType,jobbaseSalary,joburl,jobDescription))

def load_to_json(Key_work, content_arry):
    flag=True
    for i in content_arry:
        if i:
            jobTitle = i[0]
            jobEmployer = i[1]
            jobLocation = i[2]
            jobPostTime = i[3]
            jobID = i[4]
            jobskills = i[5]
            jobemploymentType = i[6]
            jobbaseSalary = i[7]
            joburl = i[8]
            jobDescription = i[9]
        
            if flag==True:
                data = {Key_work:[{
                             "jobID":jobID,
                             "jobTitle":jobTitle,
                             "jobEmployer":jobEmployer,
                             "jobLocation":jobLocation,
                             "jobPostTime":jobPostTime,
                             "jobskills":jobskills,
                             "jobemploymentType":jobemploymentType,
                             "jobbaseSalary":jobbaseSalary,
                             "joburl":joburl,
                             "jobDescription":jobDescription,
                                 }]}
                flag=False


            else:
                add_data = {    "jobID":jobID,  
                                "jobTitle":jobTitle,
                                "jobEmployer":jobEmployer,
                                "jobLocation":jobLocation,
                                "jobPostTime":jobPostTime,
                                "jobskills":jobskills,
                                "jobemploymentType":jobemploymentType,
                                "jobbaseSalary":jobbaseSalary,
                                "joburl":joburl,
                                "jobDescription":jobDescription  }
                data[Key_work].append(add_data)
    return data

def create_data(Key_work, data):
    if data:
        Job.objects.filter(Field=Key_work).delete()
        repeat_data_count = 0
        for job in data[Key_work]:
            try:
                if not Job.objects.filter(JobID=job["jobID"], Field=Key_work):
                    Job(JobID = job["jobID"],
                        Title = job["jobTitle"], 
                        Field = Key_work, 
                        Employer = job["jobEmployer"], 
                        Location = job["jobLocation"], 
                        PostTime = job["jobPostTime"], 
                        skills = job["jobskills"], 
                        employmentType = job["jobemploymentType"], 
                        baseSalary = job["jobbaseSalary"], 
                        jobDescription = job["jobDescription"], 
                        url = job["joburl"]).save()
                else:
                    repeat_data_count += 1
            except:
                print()
                traceback.print_exc()
                print()

        print("Repeat Data: %d" % repeat_data_count)
    else:
        print("Data is empty, Stop Updating " + Key_work)
