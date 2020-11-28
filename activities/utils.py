from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone

from activities.models import Action


def create_action(user, verb, target=None):
    '''
    It is a method for object creation 
    for Action model.
    '''

    #get time 1 minute backwards from now
    last_minute = timezone.now()- datetime.timedelta(seconds=60)
    #filter Actions instances if created within 1 min back from right now
    similar_actions = Action.objects.filter(
        user=user,
        verb= verb,
        created__gte=last_minute
        )

    if target:
        '''
        target is the object on action
        '''
        target_contenttype  = ContentType.objects.get_for_model(target)
        #filter similar action for the specific object
        similar_actions = similar_actions.filter(
            target_contenttype = target_contenttype ,
            target_id=target.id
            )
    
    if not similar_actions:
        '''
        if no similar action on object is found
        i.e fresh action within 1 min boundary
        create object with given arguments
        '''
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False