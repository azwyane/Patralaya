from django.contrib import admin
from activities.models import (
                                Action,Comment,Clap,
                                ViewsCount,SharesCount
                            )


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=["creator","content_object","created_on"]
    list_display_links=["creator"]
    list_filter=["created_on"]
   
    
    class meta:
        model = Comment

admin.site.register(Clap)
admin.site.register(SharesCount)
admin.site.register(ViewsCount)    