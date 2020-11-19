from django.urls import path
from events.views import (
    home, BundleCreateView,
    BundleListView, BundleDetailView,
    BundleUpdateView, BundleDeleteView,
    )

urlpatterns=[
    path('',home,name='home'),
    path('create/<int:pk>',BundleCreateView.as_view(),name='create_bundle'),
    path('list/',BundleListView.as_view(),name='list_bundle'),
    path('detail/<int:pk>',BundleDetailView.as_view(),name='detail_bundle'),
    path('update/<int:pk>',BundleUpdateView.as_view(),name='update_bundle'),
    path('delete/<int:pk>',BundleDeleteView.as_view(),name='delete_bundle'), 
    
]