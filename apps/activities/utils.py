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


from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone

from activities.models import Action


def create_action(profile, verb, target=None):
    '''
    It is a method for object creation 
    for Action model.
    '''

    #get time 1 minute backwards from now
    last_minute = timezone.now()- datetime.timedelta(seconds=60)
    #filter Actions instances if created within 1 min back from right now
    similar_actions = Action.objects.filter(
        profile = profile.pk,
        verb = verb,
        created__gte = last_minute
        )

    if target:
        '''
        target is the object on action
        '''
        target_contenttype  = ContentType.objects.get_for_model(target)
        #filter similar action for the specific object
        similar_actions = similar_actions.filter(
            target_contenttype = target_contenttype ,
            target_id=target.pk
            )
    
    if not similar_actions:
        '''
        if no similar action on object is found
        i.e fresh action within 1 min boundary
        create object with given arguments
        '''
        action = Action(profile=profile, verb=verb, target=target)
        action.save()
    