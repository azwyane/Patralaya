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

from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404,redirect
from services.forms import ShareForm
from events.models import Bundle
from profiles.models import Profile
from services.models import ReadingList
from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,
    DeleteView,TemplateView,
    View
    )
from taggit.models import Tag
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse,reverse_lazy
from services.forms import ReadingsListForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from events.mixins import CreateActivityMixin,BundleEditMixin
from django.utils.decorators import method_decorator

decorators = [ajax_required, require_POST]

@method_decorator(decorators, name='dispatch')
class Share(View):
    def post(self,request):
        try:
            slug = request.POST['slug']
            bundle = Bundle.objects.get(
                slug=slug, status='Publish')
            
            sender = request.POST['sender']
            receiver = request.POST['receiver']
            description = request.POST['description'] 
            get_bundle_url = request.build_absolute_uri(bundle.get_absolute_url())
            #preparing msg template
            subject = "WELCOME FROM PATRALAYA"
            message = f'''
            WELCOME FROM PATRALAYA 
            This bundle was shared to you from PATRALAYA
            
            {sender} recommended this paper/bundle to {receiver}
            
            MESSAGE: {description}
            
            Read {bundle.title} at {get_bundle_url}
            Visit PATRALAYA for more 
            '''
            
            send_mail(subject, message, 'tunechibaral@gmail.com', [receiver])
            return JsonResponse({'status':'ok'})
        
        except Exception as e:
            return JsonResponse({'status':'error'})
        
        return JsonResponse({'status':'error'})


class TagListView(ListView):
    model = Bundle
    template_name = 'services/tag_list.html'
    ordering = ['-created_on']
    paginate_by = 2

    def get_queryset(self):
        obj_list = super().get_queryset()
        tag = None 
        if self.kwargs:
            if self.kwargs['tag_slug']:
                tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
                obj_list = obj_list.filter(tags__in=[tag])
          
                return obj_list
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tagged_with'] = self.kwargs['tag_slug']
        return context

class SearchBundleListView(TemplateView):
    template_name = 'services/search_list.html'

    def published(self, *args, **kwargs):
        published_bundles = Bundle.published.all()
        query = self.request.GET.get('query')
        from django.db.models import Q
        published_bundles = published_bundles.filter(
            Q(title__icontains=query) | Q(context__icontains=query)
            )
        paginator = Paginator(published_bundles,4)
        page = self.request.GET.get('page')
        published_bundles = paginator.get_page(page)
        return {'published_bundles':published_bundles,'query':query}


class ReadingsListView(ListView):
    model = ReadingList
    context_object_name = 'readings'
    template_name = 'services/readings_list.html'


class ReadingsDetailView(DetailView):
    model = ReadingList
    context_object_name = 'reading'
    template_name = 'services/readings_detail.html'



class ReadingsCreateView(LoginRequiredMixin, CreateActivityMixin,SuccessMessageMixin,CreateView):
    model = ReadingList
    context_object_name = 'reading'
    template_name = 'services/readings_form.html'
    form_class = ReadingsListForm
    success_message = "You have successfully created %(title)s ReadingList, Cheers!"
    

    def form_valid(self,form):
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        form_saved = super().form_valid(form)
        # self.create_published_action()
        return form_saved    



class ReadingsUpdateView(LoginRequiredMixin,UserPassesTestMixin, CreateActivityMixin,SuccessMessageMixin,UpdateView):
    model = ReadingList
    context_object_name = 'reading'
    template_name = 'services/readings_form.html'
    form_class = ReadingsListForm
    success_message = "You have successfully updated %(title)s ReadingList"
    
    def form_valid(self,form):
        form.instance.creator = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to update it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False  


class ReadingsDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,CreateActivityMixin,DeleteView):
    model = ReadingList
    context_object_name = 'reading'
    template_name = 'services/readings_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to update it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False 

#Todo: task (install reportlab==3.5.59)
# def download_bundle(request,id):
#     if a:= Bundle.objects.get(id=id):
#         title = a.get_dict()['title']
#         context = a.get_dict()['context']
#         import io
#         from django.http import FileResponse
#         from reportlab.pdfgen import canvas
#         buffer = io.BytesIO()
#         pdf_object = canvas.Canvas(buffer,'A4')
#         #here
#         pdf_object.showPage()
#         pdf_object.save()
#         buffer.seek(0)
#         return FileResponse(buffer, as_attachment=True, filename=f'{title}-retrieved-from-Patralaya.pdf')


#ajax views

from django.utils.decorators import method_decorator

decorators = [ajax_required,require_POST]

@method_decorator(decorators, name='dispatch')
class AutoSuggestions(View):
    def post(self,request):
        query = request.POST['query']
        from django.contrib.auth import get_user_model
        from django.db.models import Q
        users = get_user_model().objects.filter(
                    Q(username__icontains=query) | Q(first_name__icontains=query)
                ).values_list('username',flat=True)
            
        bundles = Bundle.published.filter(
                    Q(title__icontains=query)
                    | Q(context__icontains=query)
                    | Q(tags__name__icontains=query),
                ).values_list('title',flat=True)
        
        from itertools import chain
        data_list = list(chain(users,bundles))
        return JsonResponse(data_list,safe=False)



@method_decorator([ajax_required,require_POST,login_required], name='dispatch')
class ReadingListAvailable(View):
    def post(self,request):
        query = request.POST['query']
        profile = Profile.objects.get(user=request.user)
        from django.db.models import Q
        readinglist = profile.readinglist_creator.filter(
                    Q(title__icontains=query)
                ).values_list('title',flat=True)
            
        bundles = Bundle.published.filter(
                    Q(title__icontains=query)
                    | Q(context__icontains=query)
                    | Q(tags__name__icontains=query),
                ).values_list('title',flat=True)
        
        from itertools import chain
        data_list = list(chain(users))
        return JsonResponse(data_list,safe=False)


@method_decorator([ajax_required,require_POST,login_required], name='dispatch')
class AddToList(View):
    def post(self,request):
        bundle_id = request.POST['bundle_id']
        reading_list_name = request.POST['reading_list_name']
        bundle = Bundle.published.filter(id=bundle_id)
        profile = Profile.objects.get(user=request.user)
        try:

            if reading_list_name in profile.readinglist_creator.values_list('title',flat=True):
                readinglist = profile.readinglist.filter(title=reading_list_name)
                readinglist.bundles.add(bundle)
                readinglist.save()
                return JsonResponse({'status':'ok'})
                
            else:
                new_list = ReadingList.objects.create(title=reading_list_name,creator=profile)
                new_list.bundles.add(bundle)
                new_list.save()
                return JsonResponse({'status':'ok'})

        except Profile.DoesNotExist:
            return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})   
        
        
       
                
        