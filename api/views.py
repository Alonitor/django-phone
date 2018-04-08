from rest_framework import viewsets
from contacts.models import Contact
from .serializers import ContactSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

# OH
#from snippets.models import Snippet
#from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.generic.base import View
from django.http import HttpResponse

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer       
    
    filter_backends = ( filters.SearchFilter, DjangoFilterBackend, )
    #filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sync',)
    search_fields = ('vcard',)

