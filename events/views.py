from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,   # require login to access the content
    UserPassesTestMixin   # check if the logged in user is owner of the object
)

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

# contrib.auth User model
from django.contrib.auth.models import User

#taggit
from taggit.models import Tag

# local models
from profiles.models import Profile
from events.models import Bundle,Comment



def home(request):
    '''
    This is the view for main landing page
    for the web app.
    '''
    return render(request,'events/home.html')


class BundleCreateView(LoginRequiredMixin, CreateView):
    '''
    - View to create a bundle: inherits from CreateView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Bundle
    template_name = 'events/bundle_form.html'
    fields = ['title','tags','context','media_image','status']
    login_url = 'home'

    def form_valid(self,form):
        '''
        save the data obtained from the form
        if its valid
        '''
        #foreign key traces parent table
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class BundleListView(ListView):
    '''
    - View to see list of bundles: inherits from ListView
    - Login is required to create bundle: inherits from LoginRequiredMixin

    Private bundle list view: returns both draft and published bundles 
    for the right owner profile else will return only published bundles 
    '''
    
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    login_url = 'home'
    
    def get_queryset(self):
        obj_list = super().get_queryset()
        if self.request.user.is_authenticated:
            if Profile.objects.get(user=self.request.user) == Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])):
                '''
                Return all private(draft) and public(publish) bundles if the user 
                requesting is the owner of the bundle
                '''
                return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))
                    )
            else: 
                '''
                Return all private(draft) and public(publish) bundles if the user 
                requesting is the owner of the bundle
                '''
                return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])),
                    status='Publish') 
        else:
            return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])),
                    status='Publish') 


class BundleDetailView(LoginRequiredMixin, DetailView):
    '''
    - View to see details in a bundle: inherits from DetailView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Bundle 
    template_name = 'events/bundle_detail.html'
    login_url = 'home'

    def get_queryset(self):
        obj_list = super().get_queryset()
        if Profile.objects.get(user=self.request.user) == Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])):
            return obj_list
        else:
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
    fields = ['title','tags','context','media_image','status']
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
    success_url = reverse_lazy('list_bundle')
    login_url = 'home'

    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to delete it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False


class PublicBundleListView(ListView):
    '''
    - View to see list of public (publish) bundles: inherits from ListView
    '''
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    login_url = 'home'

    def get_queryset(self):
        obj_list = super().get_queryset()
        tag = None 
        if self.kwargs:
            if self.kwargs['tag_slug']:
                tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
                obj_list = obj_list.filter(tags__in=[tag])
          
        return obj_list


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''
    - View to create a comment to a bundle: inherits from CreateView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Comment
    template_name = 'events/comment_form.html'
    fields = ['context']
    login_url = 'home'

    def form_valid(self,form):
        '''
        save the data obtained from the form
        if its valid
        '''
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        form.instance.bundle = Bundle.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)