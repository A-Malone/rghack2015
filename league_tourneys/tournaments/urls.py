from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.TournamentDetailView.as_view(), name='tournament'),    
    url(r'^create/$', views.create_tournament, name='create_tournament'),
    url(r'^(?P<tournament_id>[0-9]+)/add_team/$', views.create_team, name='create_team'),
    url(r'^/notification', views.notification, name='notification'),
]
