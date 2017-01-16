from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^clients/$', views.ClientList.as_view()),
    url(r'^client/(?P<pk>[0-9]+)/$', views.ClientDetail.as_view()),
    url(r'^client/(?P<client>[0-9]+)/connections/$', views.ClientConnections.as_view()),
    url(r'^client/(?P<client>[0-9]+)/commands/$', views.ClientCommands.as_view()),
    url(r'^client/(?P<client>[0-9]+)/results/$', views.ClientResults.as_view())
]

