import random
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

from .urlshortener import *

from .models import Job

domain_name = 'https://www.dice.com'
Key_location = 'New York, NY'


## page 1-30
def steeve_crawler(Key_work):
    
    herf = []
    # print('Deal page 1')
    response_page = requests.get('https://www.dice.com/jobs/q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-'+str(1)+'-jobs?')
    soup = BeautifulSoup(response_page.text,'lxml')
    # page contains 30 url
    i = random.randint(0, 29)
    # for i in range(start, start+3):
    herf.append(domain_name + soup.find("",{"id":"position"+str(i)}).get('href'))

    output = ""

    for i,work in enumerate(herf):
        try:
            response_work = requests.get(work)
            soup = BeautifulSoup(response_work.text,'lxml')
            jobTitle = soup.find("",{"class":"jobTitle"}).text
            jobEmployer = soup.find("",{"class":"employer"}).text.replace('\n','').replace('\t','')
            jobLocation = soup.find("",{"class":"location"}).text.replace('\n','')
            jobPostTime = soup.find("",{"class":"posted hidden-xs"}).text
            out = []
            foo = soup.find_all("",{"class":"row job-info"})
            for o in foo:
                out.append(o.text.replace('\n','').replace('\t',''))
                
        except AttributeError:
            jobTitle='None'
            jobEmployer='None'
            jobLocation='None'
            jobPostTime='None'
            foo='None'
            
        try:
            skills = out[0]
            employmentType = out[1]
            baseSalary = out[2]   
        except IndexError:
            skills = 'None'
            employmentType = 'None'
            baseSalary = 'None'

        str1 = str(soup.find("",{"id":"jobdescSec"}))
        soup = BeautifulSoup(str1.replace('<br/>','\n'),'lxml')
        jobDescription = soup.text
        url = get_shortenUrl(requests.utils.requote_uri(work))

        Job(Title = jobTitle, 
            Field = Key_work, 
            Employer = jobEmployer, 
            Location = jobLocation, 
            PostTime = jobPostTime, 
            skills = skills, 
            employmentType = employmentType, 
            baseSalary = baseSalary, 
            jobDescription = jobDescription, 
            url = url).save()

        output += "Title:\n" + jobTitle + "\n" + \
                "\nField:\n" + Key_work + "\n" + \
                "\nEmployer:\n" + jobEmployer + "\n" + \
                "\nLocation:\n" + jobLocation + "\n" + \
                "\nPostTime:\n" + jobPostTime + "\n" + \
                "\nskills:\n" + skills + "\n" + \
                "\nemploymentType:\n" + employmentType + "\n" + \
                "\nbaseSalary:\n" + baseSalary + "\n" + \
                "\nurl:\n" + url
                # "\njobDescription:\n" + jobDescription + \

    return output