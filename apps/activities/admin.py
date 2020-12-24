from django.contrib import admin
from activities.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)