from django.contrib import admin
from activities.models import (
                                Action,Comment,Clap,
                                Fork,Follow,ViewsCount,
                                SharesCount
                            )


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

admin.site.register(Comment)
admin.site.register(Clap)
admin.site.register(Fork)
admin.site.register(Follow)
admin.site.register(SharesCount)
admin.site.register(ViewsCount)    