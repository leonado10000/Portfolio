from django.contrib import admin
from .models import bronzelogs

class bronzelogsAdmin(admin.ModelAdmin):
    list_display = ('pk','userip', 'user', 'actionmessage', 'source', 'timestamp')
    search_fields = ('userip', 'user', 'actionmessage', 'source')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

admin.site.register(bronzelogs, bronzelogsAdmin)