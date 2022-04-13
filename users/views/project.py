from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from users.models import Tag, Project, Review, Like
from users.forms import ProjectForm, ReviewForm


# Projects
def projects(request):
    
    keyword = request.GET.get('q') or ''               # getting input from search form 
    project = keyword                                  # storing result into form input

    tags = Tag.objects.filter(name__icontains=keyword) # getting tags

    projects = Project.objects.distinct().filter(
        Q(title__icontains       = keyword) | 
        Q(description__icontains = keyword) |
        Q(owner__name__icontains = keyword) |
        Q(tags__in               = tags)
    )                                                  # filtering project

    count = projects.count()                           # getting projects count

    #pagination 
    paginator   = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context = {'projects':page_obj, 'count':count, 'page_obj':page_obj, 'heading':'Find Projects', 'value':project, 'placeholder':'projects...'}
    return render(request, 'users/projects.html', context)

# View project
def project(request, pk):
    project = get_object_or_404(Project, id=pk) 
    tags    = project.tags.all()
    reviews = project.review_set.all()
    likes   = Like.objects.filter(project=project)
    like_count = 0
    for like in likes:
        like_count += like.like
        
    form    = ReviewForm()
    
    if request.method == 'POST':                      # storing projects reviews
        form    = ReviewForm(request.POST)
        review  = form.save(commit=False)
        review.owner    = request.user.profile
        review.project  = project
        review.save()
        return redirect('project', pk=project.id)

    context = {'project':project, 'tags':tags, 'reviews':reviews, 'like_count':like_count,'likes':likes, 'form':form}
    return render(request, 'users/project.html', context)
    
# Create project
@login_required()
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':  
        form    = ProjectForm(request.POST)
        project = form.save(commit=False)
        project.owner = request.user.profile
        project.save()
        messages.success(request, 'Project added!')
        return redirect('profile', pk=request.user.profile.id)
    context = {'form':form, 'name':'Add Project'}
    return render(request, 'users/form_project.html', context)

# Edit project
@login_required()
def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk)

    # if project not created by project owner
    if request.user != project.owner.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('project', pk=project.id)
            
    context = {'form':form, 'name':'Edit Project'}
    return render(request, 'users/form_project.html', context)

# Delete project
@login_required()
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk)

    # if project not created by project owner
    if request.user != project.owner.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        project.delete()
        return redirect('profile', pk=request.user.profile.id)

    context = {'object':project.title}
    return render(request, 'form_delete.html', context)

# Edit review
@login_required()
def edit_review(request, pk):
    review = get_object_or_404(Review, id=pk)
     
    # if review not given by review author
    if request.user != review.owner.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated!')
        return redirect('project', pk=review.project.id)
    
    context = {'form':form}
    return render(request, 'users/review.html', context)

# Delete review
@login_required()
def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)

    # if review not given by review author
    if request.user != review.owner.user:
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        review.delete()
        return redirect('project', pk=review.project.id)

    context = {'object':review}
    return render(request, 'form_delete.html', context)

# Like and Unlike project
@login_required()
def rate_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    try:
        # getting user like 
        like = Like.objects.get(user=request.user.profile, project=project)
        like.delete()
    except:
        # creating user like 
        like = Like.objects.create(user=request.user.profile, project=project)
        like.like += 1
        like.save()
        
    return redirect('project', pk=project.id)
     


