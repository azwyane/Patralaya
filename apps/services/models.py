# django model fields
from django.db import models
from profiles.models import Profile
from events.models import Bundle
import uuid
from django.urls import reverse
from taggit.managers import TaggableManager


class ReadingList(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='readinglist_creator',
        )
    bundles = models.ManyToManyField(
        Bundle,
        )
    tags = TaggableManager()
  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('readinglists_detail', kwargs={'pk':self.uuid})

    class Meta:
        ordering = ['-created_on']