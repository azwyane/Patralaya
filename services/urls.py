from django.urls import path

from services.views import share

urlpatterns=[

    # shareform
    path('share/<slug:slug>/',share,name='share_by_email'),
]