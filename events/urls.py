from django.urls import path, re_path
from events.views import (
    HomeView, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    TagListView, SearchBundleListView,
    CommentBundle, ForkBundle,
    ClapBundle,
    )

# profile views is imported here to make url as example.com/<username>    
from profiles.views import user_detail

#rss feed generator
from .feeds import PublishedBundleFeed

# app_name = 'events'

urlpatterns=[

    # home url
    path('',HomeView.as_view(),name='home'),

    #user url will be example.com/<username>
    path('<slug:username>/',user_detail, name='user_detail'),

    #user action urls
    path('<slug:creator>/create/',BundleCreateView.as_view(),name='create_bundle'),
    path('<slug:creator>/all/',BundleListView.as_view(),name='list_bundle'),
    path('<slug:creator>/<slug:slug>/',BundleDetailView.as_view(),name='detail_bundle'),
    path('<slug:creator>/<slug:slug>/update/',BundleUpdateView.as_view(),name='update_bundle'),
    path('<slug:creator>/<slug:slug>/delete/',BundleDeleteView.as_view(),name='delete_bundle'), 
    
    #comment urls uses ajax 
    path('bundle/create/comment/',CommentBundle.as_view(),name='comment_bundle'),


    #public topics by tag
    path('bundle/topics/<slug:tag_slug>/',TagListView.as_view(), name='list_tag'),

    #search public bundles
    path('bundle/public/search/',SearchBundleListView.as_view(), name='search_bundle_results'),

    #rss url
    path('bundle/published/all/feed.xml', PublishedBundleFeed(), name='bundle_feed'),
    
    #fork bundles
    path('bundle/fork/new/',ForkBundle.as_view(), name='fork_bundle'),

    #fork bundles
    path('bundle/clap',ClapBundle.as_view(), name='bundle_clap'),

]