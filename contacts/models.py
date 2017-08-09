from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField()
    sync = models.NullBooleanField()

    def __str__(self):
        return 'Contact: ' + self.name
