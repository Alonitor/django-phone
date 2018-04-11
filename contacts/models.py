from django.db import models
import vobject
import uuid
from radicale.storage import random_uuid4
import json
import os
import datetime

class Contact(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField(blank=True)
    sync = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # path = models.TextField('Path', unique=True)
    #path = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    path = models.TextField(blank=True)
    collection = models.TextField('Collection', default='/pim/odd/addresses/')
    etag = models.TextField(blank=True)
    # uid = models.UUIDField()

    def __str__(self):
        return 'Contact: ' + self.name

    def uid(self):
        return os.path.splitext(self.path)[0]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        j = vobject.vCard()
        j.add('n')
        j.n.value = vobject.vcard.Name(family=self.name, given=self.name)
        j.add('fn')
        j.fn.value = self.name
        j.add('uid')
        j.uid.value = os.path.splitext(self.path)[0]
        j.add('rev')
        j.rev.value = datetime.datetime.strftime(datetime.datetime.now(), '%a, %d %b %Y %H:%M:%S %z')

        vcard_json = json.dumps(j.serialize())
        # self.vcard = j.serialize()
        self.vcard = vcard_json

        self.path = random_uuid4() + '.vcf'
        self.etag = random_uuid4()

        super().save()


        super().save()
