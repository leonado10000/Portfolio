from django.db import models

# Create your models here.
class Visitor(models.Model):
    ipaddress = models.CharField(max_length=50)
    useragent = models.CharField(max_length=1000, null=True)
    acceptedlanguage = models.CharField(max_length=1000, null=True)
    acceptedencoding = models.CharField(max_length=1000, null=True)