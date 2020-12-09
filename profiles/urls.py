from django.urls import path, reverse_lazy
from profiles.views import (
    signup, user_list,
    user_settings, user_follow,
)

#generic auth views provided by django contrib app
import django.contrib.auth.views as auth_views

urlpatterns=[

    #urls will be following pattern as example.com/profiles/<actions>
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('users/',user_list, name='user_list'),
    path('settings/',user_settings, name='profile_settings'),
    path('user/follow/',user_follow, name='user_follow'),

    #password reset views
    
    #only if user is logged in
    path('update-password/',auth_views.PasswordChangeView.as_view(success_url = reverse_lazy('password_reset_complete')),
        name='password_update_form'
        ),
    #email form 
    path(
        'change-password/submit/',
        auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'),
        name='password_reset_form'
        ),
    
    #is form is valid 
    path(
        'change-password/submit/done',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_form_submitted.html'),
        name='password_reset_done'
        ),
    
    #url from email
    path(
        'change-password/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_verified.html'),
        name='password_reset_confirm'),
    
    #on successful reset
    path(
        'change-password/success/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_completed.html'),
        name='password_reset_complete'),
] 