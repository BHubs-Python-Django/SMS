from django.db import models


class Notice(models.Model):
    notice_title = models.CharField(max_length=255)
    notice_description = models.TextField()
    notice_from = models.CharField(max_length=200)
    notice_create = models.DateTimeField(auto_now_add=True)
    notice_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notice_title


