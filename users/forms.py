from django import forms
from django.forms import ModelForm 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  
from .models import Profile, Skill, Project, Review, Message
  
class UserAccountForm(ModelForm):
    avatar = forms.ImageField(label='Avatar', required=False, error_messages = {'invalid':"Image files only"}, widget=forms.FileInput)

    resume = forms.FileField(label='Resume', required=False, error_messages = {'invalid':"Files only"}, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['avatar', 'resume','username', 'name', 'email', 'intro', 'looking_for', 'bio', 'github', 'linkedin', 'website', 'location']
        labels = {
            'name':'Full Name',
            'bio':'About',
        }  
    
    # Readonly field
    def __init__(self, *args, **kwargs):
        super(UserAccountForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
        
class UserSkillForm(ModelForm):
    
    class Meta:
        model = Skill
        fields = ['name']

class ProjectForm(ModelForm):
    featured_image = forms.ImageField(label='Featured Image', required=False, error_messages = {'invalid':"Image files only"}, widget=forms.FileInput)

    class Meta:
        model = Project
        fields = ['featured_image', 'title', 'description', 'link', 'tags']

class ReviewForm(ModelForm):
    class Meta:
        model   = Review
        fields  = ['review']
        widgets = {
            "review":forms.Textarea(attrs={'rows':5, 'required':True})
        }

class MessageForm(ModelForm):
    class Meta:
        model  = Message
        fields = ['sender_name', 'subject', 'body']
        labels = {
            'sender_name':'Your Name'
        }
