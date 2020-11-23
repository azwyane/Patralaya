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
        #creator takes the instance from profile(foreignkey can reverse reference but not oneToone)
        form.instance.creator  = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class BundleListView(ListView):
    '''
    - View to see list of bundles: inherits from ListView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''
    # queryset gets published (filtered) bundle  
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    login_url = 'home'


class BundleDetailView(LoginRequiredMixin, DetailView):
    '''
    - View to see details in a bundle: inherits from DetailView
    - Login is required to create bundle: inherits from LoginRequiredMixin
    '''

    model = Bundle 
    template_name = 'events/bundle_detail.html'
    login_url = 'home'


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
    # queryset gets published (filtered) bundle  
    # queryset = Bundle.published.all() 
    model = Bundle
    template_name = 'events/bundle_list.html'
    ordering = ['-created_on']
    paginate_by = 2
    login_url = 'home'

    def get_context_data(self,tag_slug=None, **kwargs):
        obj_list = super().get_context_data(**kwargs)
        obj_list = obj_list.filter(status='Publish')
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            obj_list = obj_list.filter(tags__in=[tag])
            obj_list['tag'] = tag
            print(obj_list)
        return obj_list

def public_bundle_view(request, tag_slug=None):
    obj_list = Bundle.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])
    return render(request,'events/bundle_list.html',{'page_obj': obj_list,'tag': tag})


