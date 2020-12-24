from django.core.mail import send_mail

from django.shortcuts import render,get_object_or_404,redirect

from services.forms import ShareForm

from events.models import Bundle

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