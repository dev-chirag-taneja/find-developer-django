from django.contrib import admin
from .models import *
import admin_thumbnails

# Register your models here.
class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1
    
class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1

@admin.register(Profile)
@admin_thumbnails.thumbnail('avatar')
class ProfileAdmin(admin.ModelAdmin):
    list_display       = ['username', 'name', 'email','date_joined', 'last_login']
    list_display_links = ['username', 'name', 'email']
    ordering           = ['-date_joined']
    search_fields      = ['username', 'name', 'email']
    list_filter        = ['last_login', 'date_joined']
    inlines            = [SkillInline, ProjectInline]
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display       = ['owner', 'name', 'created_at']
    list_display_links = ['owner', 'name']
    ordering           = ['-created_at']
    search_fields      = ['owner__name', 'name']
    list_filter        = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display       = ['title', 'link']
    list_filter        = ['tags']
    search_fields      = ['title', 'tags']
    list_display_links = ['title']
    ordering           = ['-updated_at']

admin.site.register(Tag)
admin.site.register(Message)
admin.site.register(Like)