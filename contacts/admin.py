from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','vcard','sync']
    search_fields = ['vcard']
    list_per_page = 10
     

admin.site.register(Contact,ContactAdmin)

