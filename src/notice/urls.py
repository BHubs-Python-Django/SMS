from django.conf.urls import url
from . import views


app_name = 'notice'

urlpatterns = [
    url(r'^$', views.notice_list, name='all_notice'),
    url(r'^create/$', views.add_notice, name='create_notice'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_notice, name='edit_notice'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_notice, name='delete_notice'),
]
