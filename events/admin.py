# django admin app
from django.contrib import admin

# Bundle and Comment model from events app
from events.models import Bundle, Comment
 

class BundleAdmin(admin.ModelAdmin):
    list_display=["title","creator"]
    list_display_links=["creator"]
    list_filter=["created_on"]
    
    class meta:
        model = Bundle



class CommentAdmin(admin.ModelAdmin):
    list_display=["creator","bundle","created_on"]
    list_display_links=["creator"]
    list_filter=["created_on"]
   
    
    class meta:
        model = Comment


admin.site.register(Bundle, BundleAdmin)
admin.site.register(Comment, CommentAdmin)