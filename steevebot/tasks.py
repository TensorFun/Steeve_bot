from __future__ import absolute_import, unicode_literals
from celery import task

from .daily_crawler import *
from .invalid_links_inspector import *
from .models import Job

from datetime import datetime
# import concurrent.futures
from multiprocessing import Pool
# from billiard import Pool
from .candidates_of_keyword import training_SVM

@task
def periodic_crawler():

    print("\nstart crawling the field 'Frontend' >> %s\n" % str(datetime.now()))
    daily_updater("Frontend")

    print("\nstart crawling the field 'Backend' >> %s\n" % str(datetime.now()))
    daily_updater("Backend")

    print("\nstart crawling the field 'Product management' >> %s\n" % str(datetime.now()))
    daily_updater("Product management")

    print("\nstart crawling the field 'Security' >> %s\n" % str(datetime.now()))
    daily_updater("Security")

    print("\nstart crawling the field 'Android' >> %s\n" % str(datetime.now()))
    daily_updater("Android")

    print("\nstart crawling the field 'System analyst' >> %s\n" % str(datetime.now()))
    daily_updater("System analyst")
    
    print("\nstart removing invalid links >> %s\n" % str(datetime.now()))
    remove_invalid_links()

    print("\nstart training SVM model >> %s\n" % str(datetime.now()))
    training_SVM()

    print("\nSuccess! >> %s" % str(datetime.now()))

@task
def remove_invalid_links():
    start = time.time()
    Jobs = Job.objects.all()
    print("Total : %d jobs" % Jobs.count())
    
    s = retry_remove_invalid_url(Jobs)
    cc = 1
    while not s:
        s = retry_remove_invalid_url(Jobs)
        cc += 1
    print(cc)

    renewTorIP()

    end = time.time()
    print("Total : %d jobs" % Job.objects.all().count())
    print("Removed %d jobs >>  %d sec" % (sum(s), end-start))

def retry_remove_invalid_url(Jobs):
    s = []
    renewTorIP()
    try:
        with Pool(processes=70) as pool:
            s += pool.map(remove_invalid_url, Jobs)
    except:
        s = []
    
    return s
