from django.shortcuts import render

from activities.models import Action

from profiles.models import  Profile 

def recent_activity(request):
   actions = Action.objects.exclude(profile=Profile.objects.get(user=request.user))
   return render (request,'activities/actions.html',{'actions':actions})
