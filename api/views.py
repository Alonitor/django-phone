from rest_framework import viewsets
from contacts.models import Contact
from .serializers import ContactSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer       
    
    filter_backends = ( filters.SearchFilter, DjangoFilterBackend, )
    #filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sync',)
    search_fields = ('vcard',)
