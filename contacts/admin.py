from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    fields = ['name','vcard']

admin.site.register(Contact,ContactAdmin)

