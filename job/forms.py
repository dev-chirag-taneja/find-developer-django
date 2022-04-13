from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from .models import *

class AddJobForm(ModelForm):
    class Meta:
        model   = Job
        exclude = ['author']
        labels = {
            'salary':'Salary (per month)',
            'experience':'Experience (in years)'
        }