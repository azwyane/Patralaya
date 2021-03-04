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

from feedaggregate import feedrender
# generic CRUD views in django
from django.views.generic import TemplateView, View, ListView

from feedaggregate.models import RemoteFeed
from profiles.models import Profile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# global decorator defined in common in root directory
from common.decorators import ajax_required


class FetchFeedMixin():

    def get_rendered_feed(self,url):
        feed = feedrender.render(url)
        return feed

class FeedHomeView(LoginRequiredMixin, ListView):
    model = RemoteFeed
    template_name = "feedaggregate/feed_home.html"
    context_object_name = "remote_feeds"

    def get_queryset(self):
        obj_list = super().get_queryset()
        obj_list = obj_list.filter(feed_creator=Profile.objects.get(user=self.request.user))
        return obj_list


class RemoteFeedListView(FetchFeedMixin,TemplateView):
    template_name = "feedaggregate/feed_list.html"
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        feed_id = self.kwargs['id']
        feed = RemoteFeed.objects.get(id=feed_id)
        feed_rendered = self.get_rendered_feed(feed.url)
        context['feed_info'] = feed_rendered.feed
        context['feed_body'] = feed_rendered.entries
        context['feed_id_remote'] = feed_id
        context['feed_source'] = feed.source
        context['feed_url'] = feed.url
        return context

#ajax view for Create,Update and delete and list

from django.utils.decorators import method_decorator

decorators = [ajax_required, require_POST, login_required]

@method_decorator(decorators, name='dispatch')
class CreateRemoteFeedView(View):
    def post(self,request):
        source = request.POST['source']
        action = request.POST['action']
        url = request.POST['url']
        creator = Profile.objects.get(user=request.user)
        print(source)
        if source and action and url and creator :
            try: 
                if action == 'create':
                    RemoteFeed.objects.create(
                        content_object = creator,
                        source = source,
                        url = url
                        )
                return JsonResponse({'status':'ok'})
            except RemoteFeed.DoesNotExist:
                return JsonResponse({'status':'error'})
        
        return JsonResponse({'status':'error'})


@method_decorator(decorators, name='dispatch')
class UpdateRemoteFeedView(View):
    def post(self,request):
        source = request.POST['source']
        action = request.POST['action']
        url = request.POST['url']
        feed_id = request.POST['id']
        creator = Profile.objects.get(user=request.user)
        feed = RemoteFeed.objects.get(id=feed_id,feed_creator=creator)
        
        if source and action and url:
            try: 
                if action == 'update':
                    feed.source = source
                    feed.url  = url
                    feed.save()

                return JsonResponse({'status':'ok'})
            except RemoteFeed.DoesNotExist:
                return JsonResponse({'status':'error'})
        
        return JsonResponse({'status':'error'})


@method_decorator(decorators, name='dispatch')
class DeleteRemoteFeedView(View):
    def post(self,request):
        action = request.POST['action']
        feed_id = request.POST['id']
        creator = Profile.objects.get(user=request.user)
        feed = RemoteFeed.objects.get(id=feed_id,feed_creator=creator)
        
        if feed and action:
            try: 
                if action == 'delete':
                    feed.delete()
                return JsonResponse({'status':'ok'})
            except RemoteFeed.DoesNotExist:
                return JsonResponse({'status':'error'})
        
        return JsonResponse({'status':'error'})



