from django.db import models

# Create your models here.
class bronzelogs(models.Model):
    userip = models.CharField(max_length=1000)
    user = models.CharField(max_length=100)
    actionmessage = models.CharField(max_length=1000)
    source = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

class IPProfile(models.Model):
    """
    Combined Silver/Gold layer. Tracks unique IPs, their aggregate stats, 
    and their bot status. Massively reduces row count compared to 1:1 mapping.
    """
    ip_address = models.CharField(max_length=100, unique=True)
    
    # Aggregated Stats
    total_visits = models.IntegerField(default=1)
    first_visit = models.DateTimeField()
    last_visit = models.DateTimeField()
    
    # GeoIP Data (Fetched once)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Bot Flagging
    is_auto_flagged = models.BooleanField(default=False)
    auto_flag_reason = models.CharField(max_length=255, blank=True, null=True)
    is_manual_flagged = models.BooleanField(default=None, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_bot(self):
        if self.is_manual_flagged is not None:
            return self.is_manual_flagged
        return self.is_auto_flagged

    def __str__(self):
        return f"{self.ip_address} ({self.total_visits} visits)"


# We can remove FlaggedIP and SilverLogs entirely as IPProfile replaces both.
# If Django complains about migrations, you may need to delete the migration files
# or run makemigrations and accept the deletion of the old models.