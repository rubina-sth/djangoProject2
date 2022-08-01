from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createProfile(instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

@receiver(post_save, sender=Profile)
def editUser(instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(instance, **kwargs):
    user = instance.user
    user.delete()
