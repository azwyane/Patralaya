# post_save signal for creating profile model when a user is created or updated
from django.db.models.signals import post_save

# User model from django admin
from django.contrib.auth.models import User 

# receiver to recieve the signal
from django.dispatch import receiver

# custom Profile model
from profiles.models import Profile


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()
