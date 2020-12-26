# django model fields
from django.db import models
from profiles.models import Profile
from events.models import Bundle
from activities.models import Comment,Clap
import uuid
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation

class ReadingList(models.Model):
    uuid = models.SlugField(default=uuid.uuid4,editable=False,unique=True)
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
    comments = GenericRelation(Comment,related_query_name="readings_to_comment")
    claps = GenericRelation(Clap,related_query_name="readings_to_clap")    
    tags = TaggableManager()
  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('readinglists_detail', kwargs={'pk':self.pk,'uuid':self.uuid})

    class Meta:
        ordering = ['-created_on']