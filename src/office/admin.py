from django.contrib import admin

from . import models

admin.site.register(models.ClassRoutine)
admin.site.register(models.ExamRoutine)
admin.site.register(models.Notice)
admin.site.register(models.GallaryImage)
admin.site.register(models.GallaryVideo)
admin.site.register(models.Classroom)
