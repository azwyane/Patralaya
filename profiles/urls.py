from django.urls import path
from profiles.views import (
    signup, login_user, 
    logout_user, user_list,
    user_detail, user_follow
)

urlpatterns=[
    path('login/',login_user,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',logout_user,name='logout'),
    path('users/',user_list, name='user_list'),
    path('<slug:username>/',user_detail, name='user_detail'),
    path('user/follow/',user_follow, name='user_follow'),
]