from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Job)
class Jobadmin(admin.ModelAdmin):
    list_display = ['title', 'job_type', 'location', 'experience', 'date_posted']
    search_fields = ['title', 'req_skills']
    list_filter = ['job_type', 'date_posted']
    ordering = ['-date_posted']

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['job_title',  'applied_at']
    search_fields = ['job__title']
    list_filter = ['applied_at']
    ordering = ['-applied_at']
    
    def job_title(self, obj):
        return obj.job.title
    
@admin.register(SelectedApplicant)
class SelectedApplicantAdmin(admin.ModelAdmin):
    list_display = ['job_title',  'selected_at']
    search_fields = ['job__title']
    list_filter = ['selected_at']
    ordering = ['-selected_at']
    
    def job_title(self, obj):
        return obj.job.title

