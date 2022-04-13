from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from tinymce.models import HTMLField 
import uuid

# Create your models here.

JOB_TYPE = (
    ('Remote', 'Remote'),
    ('Internship', 'Internship'),
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
    ('Internship, Part Time', 'Internship, Part Time'),
    ('Part Time, Full Time', 'Part Time, Full Time'),
)

DEGREE =  (
    ('Bachelor in CS', 'Bachelor in CS'),
    ('Bachelor Any', 'Bachelor Any'),
    ('Bachelor CS/IT/EC/ME', 'Bachelor CS/IT/EC/ME'),
    ('Master in CS', 'Master in CS'),
    ('MCA, Mtech', 'MCA, Mtech'),
    ('MCA, Mtech in CS', 'MCA, Mtech in CS'),
    ('BCA, BSC CS, Btech CS/IT', 'BCA, BSC CS, Btech CS/IT'),
    ('Btech CS/IT', 'Btech CS/IT'),
    ('Btech Any Branch', 'Btech Any Branch'),
    ('Any', 'Any'),
)
class Job(models.Model):
    id             = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author         = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title          = models.CharField(max_length=400)
    company        = models.CharField(max_length=400)
    job_type       = models.CharField(max_length=400, choices=JOB_TYPE)
    salary         = models.PositiveIntegerField(null=True, blank=True)
    location       = models.CharField(max_length=400, null=True, blank=True)
    degree         = models.CharField(max_length=400, choices=DEGREE, null=True)
    experience     = models.CharField(max_length=400, null=True, blank=True)
    description    = HTMLField(null=True)
    responsibility = HTMLField(null=True)
    req_skills     = HTMLField(null=True)
    additional     = HTMLField(null=True, blank=True)
    date_posted    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
    
class Applicant(models.Model):
    job        = models.ForeignKey(Job, on_delete=models.CASCADE)
    user       = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job}, {self.job.company}'

class SelectedApplicant(models.Model):
    job         = models.ForeignKey(Job, on_delete=models.CASCADE)
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job}, {self.job.company}'