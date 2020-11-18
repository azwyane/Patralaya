from django.urls import path
from events.views import home

urlpatterns=[
    path('',home,name='home'),
]