from django.conf.urls import url

from . import views

app_name = 'solving'
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<exercice_id>[0-9]+)/$', views.detail, name='detail'),
        url(r'^(?P<exercice_id>[0-9]+)/post_solution/$', views.postSolution, name='postSolution'),
]
