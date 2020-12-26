from django.urls import path, re_path
from events.views import (
    HomeView, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    ForkBundle, RequestAuthorshipBundle,
    AcceptAuthorshipBundle, AuthorRequestView
    )

# profile views is imported here to make url as example.com/<username>    
from profiles.views import user_detail

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
    
    #fork bundles
    path('bundle/fork/new/',ForkBundle.as_view(), name='fork_bundle'),


    #make POST request for authorship request
    path('bundle/authorship/request',RequestAuthorshipBundle.as_view(), name='bundle_authorship_request'),
    #make POST request for authorship addition/rejection
    path('bundle/authorship/request/action',AcceptAuthorshipBundle.as_view(), name='bundle_authorship_request_action'),

    path('<slug:username>/<slug:slug>/authorship/requests',AuthorRequestView.as_view(), name='bundle_authorships'),

]