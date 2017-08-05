from rest_framework import serializers
from contacts.models import Contact

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('name','vcard','url')
