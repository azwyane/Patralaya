from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,   # require login to access the content
    UserPassesTestMixin   # check if the logged in user is owner of the object
)
from django.contrib.auth.decorators import login_required

# get timezone
from django.utils import timezone

# generic CRUD views in django
from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,
    DeleteView
)

#redirects to the url
from django.urls import reverse_lazy

#function based paginator
from django.core.paginator import Paginator

# contrib.auth User model
from django.contrib.auth.models import User

#taggit
from taggit.models import Tag

# local models
from profiles.models import Profile
from events.models import Bundle,Comment

# search api from django db
from django.db.models import Q

#decorators for user comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# global decorator defined in common in root directory
from common.decorators import ajax_required

# activity generation model utils
from activities.utils import create_action

def home(request):
    '''
    This is the view for main landing page
    for the web app.
    '''
    bundles = Bundle.published.all()
    categories = Tag.objects.all()
    paginator = Paginator(bundles,3)
    page = request.GET.get('page')
    bundles = paginator.get_page(page)
    return render(request,'events/home.html',{'categories':categories,'bundles':bundles})


class BundleCreateView(LoginRequiredMixin, CreateView):
    '''
    - View to create a bundle: inherits from CreateView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Bundle
    template_name = 'events/bundle_form.html'
    fields = ['title','tags','context','media_file','media_image','status']
    login_url = 'home'

    def form_valid(self,form):
        '''
        save the data obtained from the form
        if its valid
        '''
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        # return super().form_valid(form)
        form_saved = super().form_valid(form)
        #create an action for the object
        if self.object.status == 'Publish':
            create_action(Profile.objects.get(user=self.request.user), 'created a new bundle', self.object)
        return form_saved

class BundleListView(ListView):
    '''
    - View to see list of bundles: inherits from ListView
    - Private bundle list view: returns both draft and published bundles 
      for the right owner profile else will return only published bundles 
    '''
    
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    
    def get_queryset(self):
        obj_list = super().get_queryset()
        if (self.request.user.is_authenticated and 
            Profile.objects.get(user=self.request.user) 
                == Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))):
            '''
            check if the requesting user is the owner of the bundle
            if True return all private and public bundle for the
            requesting user
            '''
            return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))
                    )
        else:
            '''
            if requesting user is not the owner of the bundle or
            is an anonymous user then return all public bundle
            of the provided username
            '''
            return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])),
                    status='Publish') 


class BundleDetailView(DetailView):
    '''
    - View to see details in a bundle: inherits from DetailView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Bundle 
    template_name = 'events/bundle_detail.html'

    def get_queryset(self):
        obj_list = super().get_queryset()
        if (self.request.user.is_authenticated and 
            Profile.objects.get(user=self.request.user) 
                == Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))):
            '''
            returns detail view for the requesting user if
            the user is the owner of the bundle
            '''
            return obj_list
        else:
            '''
            returns forced detail view only for published bundles only
            '''
            return obj_list.filter(status='Publish')


class BundleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    - View to update a bundle: inherits from UpdateView
    - Login is required to create bundle: inherits from 
        LoginRequiredMixin
    - User needs to verify if they are the owner of the bundle 
        to get access to update: inherits from UserPassesTestMixin
    '''

    model = Bundle
    fields = ['title','tags','context','media_file','media_image','status']
    template_name = 'events/bundle_form.html'
    login_url = 'home'

    def form_valid(self,form):
        '''
        save the data obtained from the form
        if its valid
        '''
        form.instance.creator = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to update it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False


class BundleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    - View to delete a bundle: inherits from DeleteView
    - Login is required to create bundle: inherits from 
        LoginRequiredMixin
    - User needs to verify if they are the owner of the bundle 
        to get access to delete: inherits from UserPassesTestMixin
    '''

    model = Bundle
    template_name = 'events/bundle_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'home'

    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to delete it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False


class TagListView(ListView):
    '''
    - View to see list of public (publish) bundles: inherits from ListView
    '''
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


class SearchBundleListView(ListView):
    model = Bundle
    template_name = 'events/search_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_bundles = Bundle.published.all()
        published_bundles = published_bundles.filter(
            # Q(title__icontains=self.request.GET['query']) | Q(context__icontains=self.request.GET['query'])
            Q(title__icontains=self.request.GET['query'])
            )
        context['published'] = published_bundles
        return context


# @login_required
# def fork_bundle(request,**kwargs):
    #   '''
    #   a fork view soon to be implemented
    #   '''
#     return render(request,'events/bundle_form.html',form)


@ajax_required
@require_POST
@login_required
def bundle_comment(request):
    pk = request.POST['pk']
    action = request.POST['action']
    context = request.POST['context']
    if pk and action and context:
        try:
            bundle_to_comment = Bundle.objects.get(
                pk=pk
                )
            if action == 'comment':
                Comment.objects.create(
                    bundle = bundle_to_comment,
                    creator=Profile.objects.get(user=request.user),
                    context=context
                    )
            
            return JsonResponse({'status':'ok'})
                
        except Profile.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})