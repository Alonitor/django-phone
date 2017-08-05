from django.db import models

class Contacts(models.Model):
    name = models.CharField(max_length=50)
    vcard = models.TextField()
