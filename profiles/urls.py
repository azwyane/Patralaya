from django.urls import path
from profiles.views import (
    signup, login_user, 
    logout_user, user_list,
    user_settings, user_follow,
)

#generic auth views provided by django contrib app
import django.contrib.auth.views as auth_views

urlpatterns=[

    #urls will be following pattern as example.com/profiles/<actions>
    path('login/',login_user,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',logout_user,name='logout'),
    path('users/',user_list, name='user_list'),
    path('settings/',user_settings, name='profile_settings'),
    path('user/follow/',user_follow, name='user_follow'),

    #password reset views

    #email form 
    path(
        'change-password/submit/',
        auth_views.PasswordResetView.as_view(template_name='profiles/reset_form.html'),
        name='password_reset_form'
        ),
    
    #is form is valid 
    path(
        'change-password/submit/done',
        auth_views.PasswordResetDoneView.as_view(template_name='profiles/reset_form_submitted.html'),
        name='password_reset_done'
        ),
    
    #url from email
    path(
        'change-password/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='profiles/reset_verified.html'),
        name='password_reset_confirm'),
    
    #on successful reset
    path(
        'change-password/success/',
        auth_views.PasswordResetCompleteView.as_view(template_name='profiles/reset_completed.html'),
        name='password_reset_complete'),
]