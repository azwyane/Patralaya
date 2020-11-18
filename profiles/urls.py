from django.urls import path
from profiles.views import signup, login_user, logout_user

urlpatterns=[
    path('login/',login_user,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',logout_user,name='logout'),
]