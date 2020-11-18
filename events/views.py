from django.shortcuts import render

def home(request):
    '''
    This is the view for main landing page
    for the web app.
    '''
    return render(request,'events/home.html')

