from django.core.mail import send_mail

from django.shortcuts import render,get_object_or_404,redirect

from services.forms import ShareForm

from events.models import Bundle

# generic CRUD views in django
from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,
    DeleteView,TemplateView,
    View
    )

#taggit
from taggit.models import Tag

#function based paginator
from django.core.paginator import Paginator

def share(request,slug):
    bundle = Bundle.objects.get(
        slug=slug, status='Publish')
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            sender = form_data['sender']
            receiver = form_data['receiver']
            description = form_data['description'] 
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
            return redirect('home')
    else:
        form = ShareForm()
    
    return render(request, 'services/share.html', {'bundle': bundle,'form': form})


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
