from django.urls import path
from activities.views import recent_activity

urlpatterns=[

    #activity stream
    path('recent/activity/notification/',recent_activity,name='recent_activity'),
]