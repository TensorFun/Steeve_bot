from .models import Job, PL, User
import random
from collections import defaultdict

#**************************************************#
# These functions are accessing to DB and get data #
#**************************************************#

# Get all unprocessing posts that crawling from dice.com
def all_data():
    jobs = Job.objects.all()
    data_dict = defaultdict(list)
    
    for job in jobs:
        data = {"JobID": job.JobID, 
                "Title": job.Title, 
                "Employer": job.Employer, 
                "Location": job.Location, 
                "PostTime": job.PostTime, 
                "skills": job.skills, 
                "employmentType": job.employmentType, 
                "baseSalary": job.baseSalary, 
                "jobDescription": job.jobDescription, 
                "url": job.url}
        data_dict[job.Field].append(data)

    return data_dict

def random_data():
    i = random.randint(0, len(Job.objects.all())-1)
    job = Job.objects.all()[i]

    return {"JobID": job.JobID, 
            "Title": job.Title, 
            "Field": job.Field, 
            "Employer": job.Employer, 
            "Location": job.Location, 
            "PostTime": job.PostTime, 
            "skills": job.skills, 
            "employmentType": job.employmentType, 
            "baseSalary": job.baseSalary, 
            "jobDescription": job.jobDescription, 
            "url": job.url}

# Get all preprocessing posts that sorted by field 
def all_PL():
    pls = PL.objects.all()
    data_dict = defaultdict(list)

    for pl in pls:
        data = {"Job": pl.Job, 
                "PL": pl.PL,
                "PL_Location": pl.PL_Location}
        
        data_dict[pl.Job.Field].append(data)

    return data_dict

# Get posts' information that suggested by NLP model
def response_suggested_jobs(suggested_jobs, suggested_field):
    data_dict = defaultdict(list)
    
    for suggested_JobID in suggested_jobs:
        job = Job.objects.get(JobID=suggested_JobID, Field=suggested_field)
        
        data = {"JobID": job.JobID, 
                "Title": job.Title, 
                "Employer": job.Employer, 
                "Location": job.Location, 
                "PostTime": job.PostTime, 
                "skills": job.skills, 
                "employmentType": job.employmentType, 
                "baseSalary": job.baseSalary, 
                "jobDescription": job.jobDescription, 
                "url": job.url}

        data_dict[suggested_field].append(data)

    return data_dict

# Get applicants' information that suggested by NLP model
def response_suggested_user(suggested_user_emails):
    response = []
    for email in suggested_user_emails:
        user = User.objects.get(email=email)
        data = {"username": user.username,
                "email": user.email, 
                "PL": user.PL}

        response.append(data)
    
    return response
