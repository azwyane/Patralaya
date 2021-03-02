'''
PATRALAYA - A Web Application for research article publishing and article aggregation.
    Copyright (C) 2020 Shrawan Baral, Sandesh Sharma

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

   contact at: debianbyte@gmail.com, sandesh0806@gmail.com
   Patralaya Copyright (C) 2020 Shrawan Baral, Sandesh Sharma
'''


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