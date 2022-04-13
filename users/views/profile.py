from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from users.models import Profile, Skill
from users.forms import UserAccountForm

# Create your views here.

# Home
def home(request):

    keyword = request.GET.get('q') or ''                   # getting input from search form 
    profile = keyword                                      # storing result into form input

    skills = Skill.objects.filter(name__icontains=keyword) # getting skills

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains   = keyword) | 
        Q(intro__icontains  = keyword) |
        Q(bio__icontains    = keyword) |
        Q(skills__in         = skills)
    )                                                       # filtering profile
    
    count = profiles.count()                                # getting profiles count
    
    # pagination 
    paginator   = Paginator(profiles, 9)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    
    context = {'profiles':page_obj, 'count':count, 'page_obj':page_obj, 'heading':'Find Developer', 'value':profile, 'placeholder':'developers...'}
    return render(request,'users/home.html', context)

# User account
@login_required()
def user_account(request):
    profile = request.user.profile
    form    = UserAccountForm(instance=profile)
    if request.method == 'POST':
        form = UserAccountForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('profile', pk=profile.id)
    context = {'form':form, 'profile':profile}
    return render(request, 'users/account.html', context)

# User profile
def user_profile(request, pk):
    profile  = Profile.objects.get(id=pk)    
    skills   = profile.skills.all()
    projects = profile.project_set.all().order_by('-created_at')

    context  ={'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/profile.html', context)

