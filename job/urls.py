from django.urls import path

from .views import *

urlpatterns = [
    # Job 
    path('', jobs ,name='jobs'),
    path('add-jobs/', add_job ,name='add_job'),
    path('<str:job_id>/', job ,name='job'),
    path('<str:job_id>/edit-job/', edit_job ,name='edit_job'),
    path('<str:job_id>/delete-job/', delete_job ,name='delete_job'),

    # Apply to Job
    path('<str:job_id>/apply/', apply, name='apply'),
    path('<str:user_id>/applied/', applied, name='applied'),
    
    # Applicants
    path('<str:job_id>/applicants/', applicants, name='applicants'),
    path('<str:job_id>/select-application/<str:user_id>/', select_application, name='select_application'),
    path('<str:job_id>/reject-application/<str:user_id>/', reject_application, name='reject_application'),
    
    # Select Applicants
    path('<str:job_id>/selected-list/', selected_list, name='selected_list'),
    path('<str:job_id>/delete_selected_list/<str:user_id>/', delete_selected_list, name='delete_selected_list'),

]