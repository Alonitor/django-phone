from django.contrib import admin
from .models import Contact

def mark_sync(modeladmin, request, queryset):
    queryset.update(sync=True)
    mark_sync.short_description = "Mark SYNC"

def mark_not_sync(modeladmin, request, queryset):
    queryset.update(sync=False)
    mark_sync.short_description = "Mark SYNC False"

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','vcard','sync']
    search_fields = ['vcard']
    list_filter = ('sync',)
    list_per_page = 10
    ordering = ['-sync']
    actions = [mark_sync,mark_not_sync]

    
admin.site.register(Contact,ContactAdmin)

