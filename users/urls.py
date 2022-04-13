from django.urls import path 

from users.views.profile import *
from users.views.skill import *
from users.views.project import *
from users.views.message import *

urlpatterns = [
    # Home
    path('', home, name='home'),

    # Profile
    path('account/',         user_account, name='account'),
    path('profile/<str:pk>/', user_profile, name='profile'),

    # Skill
    path('create-skill/',          create_skill, name='create_skill'),
    path('update-skill/<str:pk>/', update_skill, name='update_skill'),
    path('delete-skill/<str:pk>/', delete_skill, name='delete_skill'),

    # Project
    path('projects/', projects, name='projects'),
    path('projects/<str:pk>/', project, name='project'),
    path('add-project/', add_project, name='add_project'),
    path('edit-project/<str:pk>/', edit_project, name='edit_project'),
    path('delete-project/<str:pk>/', delete_project, name='delete_project'),

    # Review
    path('edit-review/<str:pk>/', edit_review, name='edit_review'),
    path('delete-review/<str:pk>/', delete_review, name='delete_review'),
    
    # Like and Unlike 
    path('project/<str:pk>/rate/', rate_project, name='rate_project'),

    # Message
    path('inbox/', inbox, name='inbox'),
    path('view-message/<str:pk>', view_message, name='view_message'),
    path('send-message/<str:pk>', send_message, name='send_message'),
]
