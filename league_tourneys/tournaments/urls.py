import django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/tournaments/(?P<pk>[0-9]+)/$', views.TournamemtDetailView.as_view(), name='tournament'),
]
