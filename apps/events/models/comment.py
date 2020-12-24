# django model fields
from django.db import models
from .bundle import Bundle
from profiles.models import Profile


# timezone
from django.utils import timezone

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