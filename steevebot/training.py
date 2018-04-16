from .models import Job, PL, User

def create_PL(PL_data):
    if PL_data:
        for data in PL_data:
            jobID, field, pl, location = data[0], data[1], data[2], data[3]       
            try:
                job = Job.objects.get(JobID=jobID, Field=field)
            except:
                print("JobDataDoesNotExist:", jobID, field, pl)
                continue
            PL.objects.create(Job=job, PL=pl, PL_Location=location)
        print("create_PL done.")
    else:
        print("PL_data is empty.")

def get_field_PL(field):
    return PL.objects.filter(Job__Field=field)


def get_applicants_PL():
    return User.objects.values_list("PL", "email")

