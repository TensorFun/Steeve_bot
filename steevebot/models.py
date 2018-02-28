from django.db import models

# Create your models here.
class Job(models.Model):
    Title = models.CharField(max_length=100)
    Field = models.CharField(blank=True, max_length=100)
    Employer = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    PostTime = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    employmentType = models.TextField(blank=True)
    baseSalary = models.CharField(max_length=100)
    jobDescription = models.TextField(blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title
        # return self.Title + "\t\t\t|\t\t\tcreated at: " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")