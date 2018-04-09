from django.db import models
import vobject
import uuid
from radicale.storage import random_uuid4
import json


class Contact(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField(blank=True)
    sync = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # path = models.TextField('Path', unique=True)
    #path = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    path = models.TextField(default=random_uuid4() + '.vcf')
    collection = models.TextField('Collection', default='/pim/odd/addresses/')
    etag = models.TextField(default=random_uuid4())

    def __str__(self):
        return 'Contact: ' + self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        j = vobject.vCard()
        j.add('n')
        j.n.value = vobject.vcard.Name(family=self.name, given=self.name)
        j.add('fn')
        j.fn.value = self.name
        vcard_json = json.dumps(j.serialize())
        # self.vcard = j.serialize()
        self.vcard = vcard_json
        super().save()


        super().save()
