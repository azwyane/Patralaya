from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils import timezone


class RemoteFeed(models.Model):
    content_type  = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 
    source = models.TextField()
    added_on = models.DateTimeField(default=timezone.now)
    url = models.URLField(blank=False)
    
    def __str__(self):
        return self.source