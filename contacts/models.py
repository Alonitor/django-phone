from django.db import models
import vobject

class Contact(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField(blank=True)
    sync = models.NullBooleanField()

    def __str__(self):
        return 'Contact: ' + self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        j = vobject.vCard()
        j.add('n')
        j.n.value = vobject.vcard.Name(family=self.name, given=self.name)
        j.add('fn')
        j.fn.value = self.name
        self.vcard = j.serialize()
        super().save()
