from rest_framework import viewsets
from contacts.models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer
