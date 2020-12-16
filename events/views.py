from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.auth.decorators import login_required

# get timezone
from django.utils import timezone

# generic CRUD views in django
from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,
    DeleteView,TemplateView,
    View
    )

#redirects to the url
from django.urls import reverse_lazy

#function based paginator
from django.core.paginator import Paginator

#taggit
from taggit.models import Tag

#models
from django.contrib.auth.models import User
# local models
from profiles.models import Profile
from events.models import (
    Bundle,
    Comment,
    Fork,
    Clap
    )

#decorators for user comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# global decorator defined in common in root directory
from common.decorators import ajax_required

#mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from events.mixins import (       #custom mixins
    BundleEditMixin, UserIsOwnerMixin, 
    CreateActivityMixin, CreateForkMixin
    )

class HomeView(TemplateView):
    template_name = "events/home.html"

    def bundles(self, *args, **kwargs):
        bundles = Bundle.published.all()
        paginator = Paginator(bundles,8)
        page = self.request.GET.get('page')
        bundles = paginator.get_page(page)
        return bundles

    def categories(self, *args, **kwargs):
        return Tag.objects.all()


class BundleCreateView(LoginRequiredMixin, CreateActivityMixin, CreateView):
    model = Bundle
    template_name = 'events/bundle_form.html'
    fields = ['title','tags','context','media_file','media_image','status','git_url']
    login_url = 'home'

    def form_valid(self,form):
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        form_saved = super().form_valid(form)
        # if self.object.status == 'Publish':
        #     create_action(Profile.objects.get(user=self.request.user), 'created a new bundle', self.object)
        self.create_published_action()
        return form_saved


class BundleListView(UserIsOwnerMixin, ListView):
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    
    def get_queryset(self):
        obj_list = super().get_queryset()
        obj_list = self.user_is_owner(obj_list)
        return obj_list


class BundleDetailView(UserIsOwnerMixin, DetailView):
    model = Bundle 
    template_name = 'events/bundle_detail.html'

    def get_queryset(self):
        obj_list = super().get_queryset()
        obj_list = self.user_is_owner(obj_list)
        return obj_list


class BundleUpdateView(LoginRequiredMixin, BundleEditMixin, UpdateView):
    model = Bundle
    fields = ['title','tags','context','media_file','media_image','status','git_url']
    template_name = 'events/bundle_form.html'
    login_url = 'login'

    def form_valid(self,form):
        form.instance.creator = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class BundleDeleteView(LoginRequiredMixin, BundleEditMixin, DeleteView):
    model = Bundle
    template_name = 'events/bundle_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'home'


class TagListView(ListView):
    model = Bundle
    template_name = 'events/tag_list.html'
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


class SearchBundleListView(TemplateView):
    template_name = 'events/search_list.html'

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


#ajax_views
from django.utils.decorators import method_decorator

decorators = [ajax_required, require_POST, login_required]

@method_decorator(decorators, name='dispatch')
class ForkBundle(CreateForkMixin,CreateActivityMixin,View):
    def post(self,request):
        pk = request.POST['pk']
        action = request.POST['action']
        new_owner = Profile.objects.get(user=request.user)
        bundle_from = Bundle.objects.get(pk=pk)            
        
        if bundle_from and action and new_owner:
            try:
                if action == 'fork':
                    self.create_bundle_fork(bundle_from,new_owner)
                    self.create_fork_action(bundle_from)
                return JsonResponse({'status':'ok'})
                    
            except Exception as e:
                return JsonResponse({'status':'error','fork_error':'No need to fork again'})
        
        return JsonResponse({'status':'error','fork_error':'No need to fork again'})


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
                        bundle = bundle_to_comment,
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
                        bundle = bundle_to_clap,
                        profile = Profile.objects.get(user=request.user)
                        )
                    self.create_clap_action(bundle_to_clap)
                else:
                    Clap.objects.filter(
                        profile = Profile.objects.get(user=request.user),
                        bundle = bundle_to_clap
                        ).delete()

                return JsonResponse({'status':'ok'})
                    
            except Bundle.DoesNotExist:
                return JsonResponse({'status':'error'})
        return JsonResponse({'status':'error'})