from django.contrib import admin
from .models import Notice


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('notice_title', 'notice_from',)

    class Meta:
        model = Notice


admin.site.register(Notice, NoticeAdmin)
