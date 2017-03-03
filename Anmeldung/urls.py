from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
    url(r'^event/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^teilnehmer/neu/(?P<pk>\d+)/$',views.teilnehmer_neu, name='teilnehmer_neu'),
]
