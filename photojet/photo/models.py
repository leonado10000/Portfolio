from django.db import models

# Create your models here.
class EVENT(models.Model):
    E_id = models.IntegerField()
    date = models.DateField()
    place = models.CharField(max_length=1000)
    photo_link = models.CharField(max_length=1000)
    desc = models.CharField(max_length=1000)
    main_topic = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Event {self.E_id} on {self.date} \n on the topic {self.main_topic} at {self.place}"