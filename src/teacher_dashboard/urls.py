from django.conf.urls import url
from teacher_dashboard import views


urlpatterns = [
    url(r'dashboard/$', views.teacher_dashboard, name='teacher_dashboard'),
    url(r'take_exam/$', views.take_exam, name='take_exam'),
    url(r'publish_result/$', views.PublishResult.as_view(), name='publish_result'),
    url(r'results/$', views.results, name='results'),
]