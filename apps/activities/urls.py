from django.urls import path
from activities.views import (
    recent_activity,CommentBundle,
    ClapBundle, user_specific_recent_activity
)

urlpatterns=[

    #activity stream
    path('recent/activity/notification/',recent_activity,name='recent_activity'),
    #user_specific ativity
    path('<slug:username>/recent',user_specific_recent_activity,name='user_specific_recent_activity'),
    #comment urls uses ajax 
    path('bundle/create/comment/',CommentBundle.as_view(),name='comment_bundle'),
    #fork bundles
    path('bundle/clap',ClapBundle.as_view(), name='bundle_clap'),
]