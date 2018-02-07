from rest_framework import viewsets
from contacts.models import Contact
from .serializers import ContactSerializer
from rest_framework import generics, filters

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer       
    
    filter_backends = ( filters.SearchFilter, filters.BaseFilterBackend, )
    filter_fields = ('sync',)
    search_fields = ('vcard',)    