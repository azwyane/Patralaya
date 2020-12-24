from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from activities.models import Action

from profiles.models import  Profile 

@login_required
def recent_activity(request):
   '''
   recent_activity is a display view that 
   return actions of the profile that
   the authenticated requesting user follows
   '''
   actions = Action.objects.exclude(profile=Profile.objects.get(user=request.user))
   following_profiles = Profile.objects.get(user=request.user).following.values_list('user',flat=True)
   if following_profiles:
      actions = actions.filter(profile__in = following_profiles)
      actions = actions[:10]
   return render (request,'activities/actions.html',{'actions':actions})
