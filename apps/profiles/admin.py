# admin app from django
from django.contrib import admin

# Profile model from profiles app
from profiles.models import Profile,Follow, Interest 

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Interest)