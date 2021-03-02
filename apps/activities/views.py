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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activities.models import Action,Clap,Comment
from profiles.models import  Profile 
from events.models import Bundle
from services.models import ReadingList
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,
    DeleteView,TemplateView,
    View
    )
from events.mixins import (       #custom mixins
    BundleEditMixin, UserIsOwnerMixin, 
    CreateActivityMixin, CreateForkMixin
    )    

# global decorator defined in common in root directory
from common.decorators import ajax_required


@login_required
def recent_activity(request):
   '''
   recent_activity is a display view that 
   return actions of the profile that
   the authenticated requesting user follows
   '''
   actions = None
   following_profiles = Profile.objects.get(user=request.user).following.values_list('user',flat=True)
   if following_profiles:
      actions = Action.objects.exclude(profile=Profile.objects.get(user=request.user)) 
      actions = actions.filter(profile__in = following_profiles)
      actions = actions[:10]
   return render (request,'activities/actions.html',{'actions':actions})


def user_specific_recent_activity(request,username):
    '''
    recent_activity is a display view that 
    return actions of the profile 
    '''
    actions = None
    # User model from django auth app
    from django.contrib.auth.models import User
    actions = Action.objects.filter(profile=Profile.objects.get(user=User.objects.get(username=username))) 
    actions = actions[:10]
    return render (request,'activities/actions.html',{'actions':actions})


#ajax views
from django.utils.decorators import method_decorator

decorators = [ajax_required, require_POST, login_required]

@method_decorator(decorators, name='dispatch')
class CommentBundle(CreateActivityMixin, View):
    def post(self,request):
        pk = request.POST['pk']
        action = request.POST['action']
        context = request.POST['context']
        bundle_to_comment = Bundle.objects.get(pk=pk)
        if bundle_to_comment and action and context:
            try: 
                if action == 'comment':
                    Comment.objects.create(
                        content_object = bundle_to_comment,
                        creator=Profile.objects.get(user=request.user),
                        context=context
                        )
                    self.create_comment_action(bundle_to_comment) 
                return JsonResponse({'status':'ok'})
                    
            except Bundle.DoesNotExist:
                return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})


@method_decorator(decorators, name='dispatch')
class ClapBundle(CreateActivityMixin, View):
    def post(self,request):
        pk = request.POST['pk']
        action = request.POST['action']
        if pk and action:
            try:
                bundle_to_clap = Bundle.objects.get(
                    pk=pk
                    )
                if action == 'clap':
                    Clap.objects.create(
                        content_object = bundle_to_clap,
                        profile = Profile.objects.get(user=request.user)
                        )
                    self.create_clap_action(bundle_to_clap)
                else:
                    Clap.objects.filter(
                        profile = Profile.objects.get(user=request.user),
                        bundle_to_clap = bundle_to_clap
                        ).delete()

                return JsonResponse({'status':'ok'})
                    
            except Bundle.DoesNotExist:
                return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})   


@method_decorator(decorators, name='dispatch')
class CommentReadingList(CreateActivityMixin, View):
    def post(self,request):
        pk = request.POST['pk']
        action = request.POST['action']
        context = request.POST['context']
        readings_to_comment = ReadingList.objects.get(pk=pk)
        if readings_to_comment and action and context:
            try: 
                if action == 'comment':
                    Comment.objects.create(
                        content_object = readings_to_comment,
                        creator=Profile.objects.get(user=request.user),
                        context=context
                        )
                    self.create_comment_action(readings_to_comment) 
                return JsonResponse({'status':'ok'})
                    
            except Bundle.DoesNotExist:
                return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})


@method_decorator(decorators, name='dispatch')
class ClapReadingList(CreateActivityMixin, View):
    def post(self,request):
        pk = request.POST['pk']
        action = request.POST['action']
        if pk and action:
            try:
                readings_to_clap = ReadingList.objects.get(
                    pk=pk
                    )
                if action == 'clap':
                    Clap.objects.create(
                        content_object = readings_to_clap,
                        profile = Profile.objects.get(user=request.user)
                        )
                    self.create_clap_action(bundle_to_clap)
                else:
                    Clap.objects.filter(
                        profile = Profile.objects.get(user=request.user),
                        readings_to_clap =readings_to_clap
                        ).delete()

                return JsonResponse({'status':'ok'})
                    
            except Bundle.DoesNotExist:
                return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})   
