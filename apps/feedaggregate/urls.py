from django.urls import path
from feedaggregate.views  import (
    RemoteFeedListView, CreateRemoteFeedView,
    UpdateRemoteFeedView, DeleteRemoteFeedView,
    FeedHomeView
)

urlpatterns=[
    
    path('fetch/feed/home/',FeedHomeView.as_view(),name='feed_home'),
    path('fetch/feed/<id>/',RemoteFeedListView.as_view(),name='feed_list_from_remote'),
   
    #ajaxviews
    path('fetch/feed/create/',CreateRemoteFeedView.as_view(),name='feed_create'),
    path('fetch/feed/update/',UpdateRemoteFeedView.as_view(),name='feed_update'),
    path('fetch/feed/delete/',DeleteRemoteFeedView.as_view(),name='feed_delete'),
]