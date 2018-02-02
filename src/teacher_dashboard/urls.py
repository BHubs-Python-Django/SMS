from django.conf.urls import url
from teacher_dashboard import views


urlpatterns = [
    url(r'dashboard/$', views.teacher_dashboard, name='teacher_dashboard'),
]