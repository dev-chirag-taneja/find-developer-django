from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from job.models import *
from job.forms import *
from users.models import *

# Create your views here.
# All Job
def jobs(request):

    keyword = request.GET.get('q') or ''               # getting input from search form 
    job = keyword                                      # storing result into form input

    jobs = Job.objects.filter(
        Q(title__icontains        = keyword) | 
        Q(description__icontains  = keyword) |
        Q(req_skills__icontains   = keyword) 
    ).order_by('-date_posted')                      # filtering profile
    
    count = jobs.count()                            # getting job count
    
    # pagination 
    paginator   = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    
    context = {'jobs':page_obj, 'count':count, 'page_obj':page_obj, 'heading':'Search Jobs', 'value':job, 'placeholder':'jobs...'}
    return render(request,'job/jobs.html', context)

# Adding Job
@login_required()
def add_job(request):
    form = AddJobForm()
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            job        = form.save(commit=False)
            job.author = request.user.profile
            job.save()
            messages.success(request, 'Job created!')
            return redirect('jobs')

    context = {'form':form, 'name':'Add Job'}
    return render(request, 'job/job_form.html', context)

# Single Job
def job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user.is_authenticated:
        applied_job = Applicant.objects.filter(user=request.user.profile, job=job).exists()
    else:
        applied_job = False
    context = {'job':job, 'applied_job':applied_job}
    return render(request, 'job/job.html', context)

# Edit Job
@login_required()
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # if job not created by job author
    if request.user != job.author.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    form = AddJobForm(instance=job)
    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)
        if form.is_valid():
            job.save()
            messages.success(request, 'Job updated!')
            return redirect('job', job_id=job.id)

    context = {'form':form, 'name':'Edit Job'}
    return render(request, 'job/job_form.html', context)

# Delete Job
@login_required()
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # if job not created by job author
    if request.user != job.author.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        job.delete()
        return redirect('jobs')

    context = {'object':job, 'title':'Delete Job | Find-Dev'}
    return render(request, 'form_delete.html', context)

# Apply to job
@login_required()
def apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    Applicant.objects.create(job=job, user=request.user.profile)
    messages.success(request, 'Apllied successfully!')
    return redirect('job', job_id=job.id)

# See user applied job
@login_required()
def applied(request, user_id):
    see_applied_job = Applicant.objects.filter(user=user_id)
    context = {'see_applied_job':see_applied_job}
    return render(request, 'job/applied.html', context)

# See job applicants
@login_required()
def applicants(request, job_id):
    job        = get_object_or_404(Job, id=job_id)
    applicants = Applicant.objects.filter(job=job)
    context = {'job':job ,'applicants':applicants}
    return render(request, 'job/applicants.html', context)

# Select applications
@login_required()
def select_application(request, job_id, user_id):
    job  = get_object_or_404(Job, id=job_id)
    user = get_object_or_404(Profile, id=user_id)
    SelectedApplicant.objects.create(job=job, user=user)
    Applicant.objects.get(job=job, user=user).delete()
    messages.success(request, 'Application selected!')
    return redirect('applicants', job_id=job.id)

# Reject apllications
@login_required()
def reject_application(request, job_id, user_id):
    job  = get_object_or_404(Job, id=job_id)
    user = get_object_or_404(Profile, id=user_id)
    Applicant.objects.get(job=job, user=user).delete()
    messages.success(request, 'Application rejected!')
    return redirect('applicants', job_id=job.id)

# See selected applicants list
@login_required()
def selected_list(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    selected_applicants = SelectedApplicant.objects.filter(job=job)
    context  = {'job':job, 'selected_applicants': selected_applicants}
    return render(request, 'job/selected.html', context)

# Delete selected applicants list
@login_required()
def delete_selected_list(request, job_id, user_id):
    job  = get_object_or_404(Job, id=job_id)
    user = get_object_or_404(Profile, id=user_id)
    SelectedApplicant.objects.get(job=job, user=user).delete()
    return redirect('selected_list', job_id=job.id)

