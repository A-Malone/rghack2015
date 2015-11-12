from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.TournamentDetailView.as_view(),
        name='tournament'),
    url(r'^/notification', views.notification, name='notification'),
]
