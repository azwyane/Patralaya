from django.urls import path
from events.views import (
    home, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    CommentCreateView,TagListView,
    )

# profile views is imported here to make url as example.com/<username>    
from profiles.views import user_detail

urlpatterns=[

    # home url
    path('',home,name='home'),

    #user url will be example.com/<username>
    path('<slug:username>/',user_detail, name='user_detail'),

    #user action urls
    path('<slug:creator>/create/',BundleCreateView.as_view(),name='create_bundle'),
    path('<slug:creator>/all/',BundleListView.as_view(),name='list_bundle'),
    path('<slug:creator>/<slug:slug>/',BundleDetailView.as_view(),name='detail_bundle'),
    path('<slug:creator>/<slug:slug>/update/',BundleUpdateView.as_view(),name='update_bundle'),
    path('<slug:creator>/<slug:slug>/delete/',BundleDeleteView.as_view(),name='delete_bundle'), 
    
    #comment urls uses ajax 
    path('<slug:creator>/<slug:slug>/comment/',CommentCreateView.as_view(),name='comment_bundle'),

    #public topics by tag
    path('bundle/topics/<slug:tag_slug>/',TagListView.as_view(), name='list_tag'),

]