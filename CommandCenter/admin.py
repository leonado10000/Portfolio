from django.contrib import admin
from .models import bronzelogs, IPProfile

class bronzelogsAdmin(admin.ModelAdmin):
    list_display = ('pk','userip', 'user', 'actionmessage', 'source', 'timestamp')
    search_fields = ('userip', 'user', 'actionmessage', 'source')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

class IPProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ip_address', 'country', 'city', 'latitude', 'longitude')
    search_fields = ('ip_address', 'country', 'city')
    list_filter = ('country', 'city')
    ordering = ('-pk',)

admin.site.register(bronzelogs, bronzelogsAdmin)
admin.site.register(IPProfile, IPProfileAdmin)