from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField 
import uuid

# Create your models here.

JOB_ROLE = (
    ('Software Development Role', 'Software Development Role'),
    ('Frontend Role','Frontend Role'),
    ('Backend Role', 'Backend Role'),
    ('FullStack Role', 'FullStack Role'),
    ('Full Time Job', 'Full Time Job'),
    ('Part Time Job', 'Part Time Job'),
    ('Internship', 'Internship'),
    ('Remote Job', 'Remote Job'),
)

class Profile(models.Model):
    id          = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username    = models.CharField(max_length=200, null=True)
    name        = models.CharField(max_length=200, null=True, blank=True)
    email       = models.EmailField(max_length=254, null=True, unique=True)
    intro       = models.CharField(max_length=400, null=True, blank=True)
    looking_for = models.CharField(max_length=200, choices=JOB_ROLE, null=True, blank=True)
    bio         = HTMLField(null=True, blank=True)
    avatar      = models.ImageField(null=True, blank=True, default="default.jpg", upload_to="images/")
    github      = models.URLField(max_length=200, null=True, blank=True)
    linkedin    = models.URLField(max_length=200, null=True, blank=True)
    website     = models.URLField(max_length=200, null=True, blank=True)
    resume      = models.FileField(upload_to='files/', null=True, blank=True)
    location    = models.CharField(max_length=200, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.id})
    
    def __str__(self):
        return self.user.username


class Skill(models.Model):
    id         = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    owner      = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='skills')
    name       = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name       = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Project(models.Model):
    id             = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    owner          = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title          = models.CharField(max_length=200)
    description    = HTMLField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='demo.jpg', upload_to='images/')
    link           = models.URLField(max_length=200, null=True, blank=True)
    tags           = models.ManyToManyField(Tag, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("project", kwargs={"pk": self.pk})


class Review(models.Model):
    id         = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    owner      = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project    = models.ForeignKey(Project, on_delete=models.CASCADE)
    review     = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.review
    
    
class Like(models.Model): 
    user       = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project    = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    like       = models.PositiveIntegerField(null=True, default=0)
  
    class Meta:
        ordering = ['-project']
    
    def __str__(self):
        return f'{self.project} - {self.like}'


class Message(models.Model):
    id          = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    sender      = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    receiver    = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='receiver')
    sender_name = models.CharField(max_length=200)
    subject     = models.CharField(max_length=1000, null=True)
    body        = HTMLField(null=True)
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_read', '-created_at']

    def __str__(self):
        return self.subject
        
    