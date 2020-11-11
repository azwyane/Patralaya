
# django model fields
from django.db import models

# factory settings
from django.conf import settings

# timezone
from django.utils import timezone

# reverse the parent content
from django.urls import reverse

# profile model
from profiles.models import Profile


class Bundle(models.Model):
    '''
    Bundle specifies a Bundle table in the database. 
    It consists of following attributes:
    - creator: foreign key to the Profile which owns the Bundle.
    - title : title is the title with which the bundle is created
    - context: context is a text field for now, consists of long ypeable text field
    - creation_date: consists of time field
    - media_image: for now it consists of the image url of the image(only one)
    '''
    creator = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='bundle',
        )
    title = models.CharField(max_length=200)
    context = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    # images get saved in the project root_directory/media/bundle_image
    media_image = models.ImageField(
        upload_to='bundle_image',
        blank=True,
        null=True
        )


    def __str__(self):
        return self.title




class Comment(models.Model):
    '''
    Comment specifies the Comment tabel in the database
    It consists of following attributes:
    - bundle: foreign key to the bundle the comment is being refered to
    - creator: foreign key to the Profile the comment is being created by 
    - title : title is the title with which the bundle is created
    - context: context is a text field for now, consists of long typeable text field
    - creation_date: consists of time field
    '''
    bundle = models.ForeignKey(
        Bundle, 
        on_delete=models.CASCADE, 
        related_name='comment',
        )
    creator = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        null=True,
        related_name='comment_profile'
        )
    context = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return f"{self.creator} : {self.context}"