from django.db import models
from django.urls import reverse

class Contact(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField()
    sync = models.NullBooleanField()

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.pk)])

    def __str__(self):
        return 'Contact: ' + self.name

    def get_content(self):
        vcard = self.vcard      
        return vcard
