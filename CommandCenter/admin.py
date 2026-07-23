from django.contrib import admin
from .models import bronzelogs, SilverLogs

class bronzelogsAdmin(admin.ModelAdmin):
    list_display = ('pk','userip', 'user', 'actionmessage', 'source', 'timestamp')
    search_fields = ('userip', 'user', 'actionmessage', 'source')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

class SilverlogsAdmin(admin.ModelAdmin):
    list_display = ('pk','userip', 'actionmessage', 'timestamp', 'country', 'city', 'latitude', 'longitude')
    search_fields = ('userip', 'actionmessage', 'country', 'city')
    list_filter = ('timestamp', 'country', 'city')
    ordering = ('-timestamp',)

admin.site.register(bronzelogs, bronzelogsAdmin)
admin.site.register(SilverLogs, SilverlogsAdmin)