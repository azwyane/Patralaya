from django.urls import path
from activities.views import recent_activity,CommentBundle,ClapBundle

urlpatterns=[

    #activity stream
    path('recent/activity/notification/',recent_activity,name='recent_activity'),
    #comment urls uses ajax 
    path('bundle/create/comment/',CommentBundle.as_view(),name='comment_bundle'),
    #fork bundles
    path('bundle/clap',ClapBundle.as_view(), name='bundle_clap'),
]