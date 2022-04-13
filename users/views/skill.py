from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Skill
from users.forms import UserSkillForm

# Create skill
@login_required()
def create_skill(request):
    profile = request.user.profile

    form    = UserSkillForm()
    if request.method == 'POST':
        form  = UserSkillForm(request.POST)
        if form.is_valid():
            skill       = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added!')
            return redirect('profile', pk=profile.id)

    context = {'form':form, 'object':'Create Skill'}
    return render(request, 'users/form_skills.html', context)

# Update skill
@login_required()
def update_skill(request, pk):
    profile = request.user.profile
    skill   = get_object_or_404(profile.skill_set, id=pk)

    form    = UserSkillForm(instance=skill)
    if request.method == 'POST':
        form  = UserSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated!')
            return redirect('profile', pk=profile.id)

    context = {'form':form, 'object':'Update Skill'}
    return render(request, 'users/form_skills.html', context)

# Delete skill
@login_required()
def delete_skill(request, pk):
    profile = request.user.profile
    skill   = get_object_or_404(profile.skill_set, id=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('profile', pk=profile.id)

    context = {'object': skill.name}
    return render(request, 'form_delete.html', context)
