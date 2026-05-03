from django.db import models

# Create your models here.
class bronzelogs(models.Model):
    userip = models.CharField(max_length=1000)
    user = models.CharField(max_length=100)
    actionmessage = models.CharField(max_length=1000)
    source = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)
