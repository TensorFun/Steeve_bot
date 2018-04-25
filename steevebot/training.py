from .models import Job, PL, User

#*********************************************************
# These functions are provide for NLP model to access DB #
#*********************************************************


# Save posts' information crawling from dice.com after preprosessing
def create_PL(PL_data):
    """
    PL_data : [[job1, field, pls, location],[job2, field, pl, location]...

    """
    if PL_data:
        PL.objects.all().delete()
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

# Get all posts that belong to a specific field
def get_field_PL(field):

    """
    input 'field' : frontend or backend ...

    output :[[job1, field, pls, location],[job2, field, pl, location]...
    """

    return PL.objects.filter(Job__Field=field)


# Get applicants' information 
def get_applicants_PL():

    """
    input ---
    output : [[pl, email_1], [pl, email_2].......]
    """
    return User.objects.values_list("PL", "email")

