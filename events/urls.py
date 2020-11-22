from django.urls import path
from events.views import (
    home, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    )

urlpatterns=[
    path('home/',home,name='home'),
    path('create/',BundleCreateView.as_view(),name='create_bundle'),
    path('list/',BundleListView.as_view(),name='list_bundle'),

    #slug is dynamically generated from the Bundle model as /<creator>/<title>
    path('<slug:creator>/<slug:slug>',BundleDetailView.as_view(),name='detail_bundle'),
    
    path('update/<slug:slug>',BundleUpdateView.as_view(),name='update_bundle'),
    path('delete/<slug:slug>',BundleDeleteView.as_view(),name='delete_bundle'), 
    
]