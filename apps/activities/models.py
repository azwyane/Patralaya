from django.db import models

#contentType represents actual model(ex: Bundle, Comment) 
#in the project apps
from django.contrib.contenttypes.models import ContentType

#accepts the names of the content-type and object-ID fields as arguments
from django.contrib.contenttypes.fields import GenericForeignKey

#profile instance which generates activities
from profiles.models import Profile


class Action(models.Model):
    '''
    The Action table records:
    - profile which is the action creator
    - verb which is the action on the object
    - targetcontenttype which is the Models from apps
    - target_id which is the instance id from the respective model 
    - target is the object on action
    - created records the time of action

    for more on contenttypes visit:https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/
    '''
    profile = models.ForeignKey(
        Profile,related_name='actions',
        db_index=True,on_delete=models.CASCADE
        )
    verb = models.CharField(max_length=255)
    target_contenttype = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
        )
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True
        )
    target = GenericForeignKey('target_contenttype', 'target_id')
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
        )
    
    class Meta:
        ordering = ('-created',)
