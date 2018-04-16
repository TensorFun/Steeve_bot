from django.db import models

# Create your models here.
class Job(models.Model):
    JobID = models.CharField(max_length=400)
    Title = models.CharField(max_length=400)
    Field = models.CharField(blank=True, max_length=400)
    Employer = models.CharField(max_length=400)
    Location = models.CharField(max_length=400)
    PostTime = models.CharField(max_length=400)
    skills = models.TextField(blank=True)
    employmentType = models.TextField(blank=True)
    baseSalary = models.CharField(blank=True, max_length=400)
    jobDescription = models.TextField(blank=True)
    url = models.URLField(blank=True, max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.Title
        return self.Title + "\t\t\t|\t\t\tcreated at: " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class PL(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    PL = models.TextField(blank=True)
    PL_Location = models.CharField(blank=True, max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Job.Title + "\t\t\t|\t\t\tcreated at: " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

class User(models.Model):
    username = models.CharField(max_length=400)
    email = models.CharField(max_length=400, primary_key=True)
    PL = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "\t\t\t|\t\t\tcreated at: " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")
