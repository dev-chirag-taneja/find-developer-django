from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user     = instance,
            username = instance.username,
            name     = instance.username + ' ',
            email    = instance.email
        )
        profile.save()

@receiver(post_save, sender=Profile)     
def update_user(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.username   = instance.username
        user.first_name = instance.name.split(' ')[0]
        user.last_name  = instance.name.split(' ')[1]  if len(instance.name.split(' ')) > 1 else ' '
        user.email      = instance.email
        user.save()

@receiver(post_delete, sender=Profile)
def delete_user(sender, instance,**kwargs):
    instance.user.delete()