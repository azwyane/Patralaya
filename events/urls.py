from django.urls import path
from events.views import (
    home, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    PublicBundleListView, TagListView,
    CommentCreateView,
   
    )
from profiles.views import user_detail

urlpatterns=[
    path('',home,name='home'),
    path('<slug:username>/',user_detail, name='user_detail'),
    path('<slug:creator>/create/',BundleCreateView.as_view(),name='create_bundle'),
    path('<slug:creator>/all/',BundleListView.as_view(),name='list_bundle'),

    #slug is dynamically generated from the Bundle model as /<creator>/<title>
    path('<slug:creator>/<slug:slug>/',BundleDetailView.as_view(),name='detail_bundle'),
    
    path('<slug:creator>/<slug:slug>/update/',BundleUpdateView.as_view(),name='update_bundle'),
    path('<slug:creator>/<slug:slug>/delete/',BundleDeleteView.as_view(),name='delete_bundle'), 
    
    #public list  
    path('all/',PublicBundleListView.as_view(),name='list_public_bundle'),
    path('all/tag/<slug:tag_slug>/',PublicBundleListView.as_view(), name='list_bundle_by_tag'),

    #comment urls
    path('<slug:creator>/<slug:slug>/comment/',CommentCreateView.as_view(),name='comment_bundle'),

    #topics by tag
    path('bundle/topics/<slug:tag_slug>/',TagListView.as_view(), name='list_tag'),

]