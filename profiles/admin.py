# admin app from django
from django.contrib import admin

# Profile model from profiles app
from profiles.models import Profile,Follow 

admin.site.register(Profile)
admin.site.register(Follow)