from django.db import models

# Create your models here.
class bronzelogs(models.Model):
    userip = models.CharField(max_length=1000)
    user = models.CharField(max_length=100)
    actionmessage = models.CharField(max_length=1000)
    source = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

class FlaggedIP(models.Model):
    """
    Central profile for an IP address to manage Auto and Manual bot flags.
    We don't ban them; we just tag them here so the dashboard can filter/highlight them.
    """
    ip_address = models.CharField(max_length=100, unique=True)
    
    # Auto-flagging managed by your Cron job heuristics
    is_auto_flagged = models.BooleanField(default=False)
    auto_flag_reason = models.CharField(max_length=255, blank=True, null=True)
    
    # Manual flagging managed by you via the Dashboard UI
    # True = Definitely a bot, False = Definitely a human (whitelist), Null = Let auto decide
    is_manual_flagged = models.BooleanField(default=None, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True, help_text="Why did you manually flag this?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_bot(self):
        """
        Logic: Manual override always wins. If no manual override, rely on Auto.
        """
        if self.is_manual_flagged is not None:
            return self.is_manual_flagged
        return self.is_auto_flagged

    def __str__(self):
        return self.ip_address


class SilverLogs(models.Model):
    """
    The processed, enriched logs used for the Dashboard and Map.
    """
    bronze_ref = models.OneToOneField(bronzelogs, on_delete=models.CASCADE)
    
    # We link the log to the IP Profile so we know if this log belongs to a bot
    ip_profile = models.ForeignKey(FlaggedIP, on_delete=models.SET_NULL, null=True, related_name='logs')
    
    userip = models.CharField(max_length=100)
    actionmessage = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()
    
    # GeoIP Data for the World Map
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.userip} ({self.country})"