from django.db import models

# Create your models here.
class projectTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    projectTopic = models.CharField(max_length=50)

    projectName = models.CharField(max_length=50, null=False, blank=False)
    projectDescription = models.CharField(max_length=500, null=False, blank=False)

    startDate = models.DateField(auto_created=True, auto_now_add=True)
    endDate = models.DateField(auto_created=True, auto_now_add=True)