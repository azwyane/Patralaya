# django admin app
from django.contrib import admin

# Bundle, Comment and Fork model from events app
from events.models import Bundle, Fork, Clap, AcceptedAuthorshipRequest, ReceivedAuthorshipRequest
 

class BundleAdmin(admin.ModelAdmin):
    list_display=["title","slug","creator","status"]
    list_display_links=["slug"]
    list_filter=["created_on"]
    prepopulated_fields = {'slug': ('title',)}
    
    class meta:
        model = Bundle



admin.site.register(Bundle, BundleAdmin)
admin.site.register(Fork)
admin.site.register(AcceptedAuthorshipRequest)
admin.site.register(ReceivedAuthorshipRequest)