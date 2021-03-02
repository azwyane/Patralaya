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