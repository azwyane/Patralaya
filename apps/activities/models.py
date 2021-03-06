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


from django.db import models

#contentType represents actual model(ex: Bundle, Comment) 
#in the project apps
from django.contrib.contenttypes.models import ContentType

#accepts the names of the content-type and object-ID fields as arguments
from django.contrib.contenttypes.fields import GenericForeignKey

#profile instance which generates activities
from profiles.models import Profile

# timezone
from django.utils import timezone

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


class Comment(models.Model):
    '''
    Comment specifies the Comment tabel in the database
    It consists of following attributes:
    - creator: foreign key to the Profile the comment is being created by 
    - title : title is the title with which the bundle is created
    - context: context is a text field for now, consists of long typeable text field
    - creation_date: consists of time field
    '''
    content_type  = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    creator = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='commented_by'
        )
    context = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return f"{self.creator} : {self.context}"

class Clap(models.Model):
    content_type  = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='clapped_by',
    )
    claped_on = models.DateTimeField(
        auto_now_add=True,
        db_index=True)

        
    class Meta:
        ordering = ('-claped_on',)


    def __str__(self):
        return f'{self.profile} claped {self.content_object}'


class CountBase(models.Model):
    content_type  = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering =['-count'] 
        abstract = True



class SharesCount(CountBase):
    def __str__(self):
        return f"{self.content_object} shared {self.count} times"


class ViewsCount(CountBase):
    def __str__(self):
        return f"{self.content_object} viewed {self.count} times"

 