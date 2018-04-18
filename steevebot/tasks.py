from __future__ import absolute_import, unicode_literals
from celery import task

from .daily_crawler import *
from .invalid_links_inspector import *
from .models import Job

from datetime import datetime
# import concurrent.futures
from multiprocessing import Pool
# from billiard import Pool
from .candidates_of_keyword import training_DNN

@task
def periodic_crawler():
    # Job.objects.all().delete()
    print("\n" + "start crawling the field 'Frontend' >> " + str(datetime.now()) + "\n")
    daily_updater("Frontend")
    print("\n" + "start crawling the field 'Backend' >> " + str(datetime.now()) + "\n")
    daily_updater("Backend")
    print("\n" + "start removing invalid links >> " + str(datetime.now()) + "\n")
    remove_invalid_links()
    print("\n" + "start training DNN model' >> " + str(datetime.now()) + "\n")
    training_DNN()
    print("\n" + "Success! >> " + str(datetime.now()))

@task
def remove_invalid_links():
    start = time.time()
    Jobs = Job.objects.all()
    print("Total : " + str(len(Jobs)) + " jobs")
    
    s = retry_remove_invalid_url(Jobs)
    cc = 1
    while not s:
        s = retry_remove_invalid_url(Jobs)
        cc += 1
    print(cc)

    renewTorIP()

    end = time.time()
    print("Total : " + str(len(Job.objects.all())) + " jobs")
    print("Removed " + str(sum(s)) + " jobs >>  " + str(end-start) + " sec")

def retry_remove_invalid_url(Jobs):
    s = []
    renewTorIP()
    try:
        with Pool(processes=70) as pool:
            s += pool.map(remove_invalid_url, Jobs)
    except:
        s = []
    
    return s
