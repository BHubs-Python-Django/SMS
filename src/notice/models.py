from django.db import models
from account.models import School


class Notice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    author = models.CharField(max_length=222)
    notice_title = models.CharField(max_length=255)
    notice_description = models.TextField()
    notice_from = models.CharField(max_length=200)
    notice_create = models.DateTimeField(auto_now_add=True)
    notice_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notice_title


