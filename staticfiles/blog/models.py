from django.db import models

# Create your models here.
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    textfield = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now=True)
    sender = models.CharField(max_length=500,null=True)
    likes = models.IntegerField(default=0)
    topic_obj = models.ForeignKey("Topics", on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}. {self.sender} ({self.time}): {self.textfield}, TOPIC:{self.topic_obj}"

class Topics(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="shaquille.oatmeal")
    descrition = models.CharField(max_length=600, blank=True)
    number_of_messages = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    image_link = models.CharField(max_length=200,default="https://www.aiscribbles.com/img/variant/large-preview/27293/?v=bf7291")

    def __str__(self) -> str:
        return f"{self.id}. {self.name}"