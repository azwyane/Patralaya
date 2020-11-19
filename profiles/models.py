# django model fields
from django.db import models

# factory settings
from django.conf import settings

# User model from django auth app
from django.contrib.auth.models import User

# timezone
from django.utils import timezone

# reverse the parent content
from django.urls import reverse


class Profile(models.Model):
    '''
    Profile specifies the Profile table in the database.
    Here the attributes are:
    - user: foreign key to User model defined in the admin app
    - profile_picture: image of the profile

    It refers to the social profile of the user. These fields are
    extensible for future.
    '''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
        )
    profile_picture = models.ImageField(
        default='default.jpeg',
        upload_to='profile_picture',
        )
 

    def __str__(self):
        return f"{self.user.username}"
    


