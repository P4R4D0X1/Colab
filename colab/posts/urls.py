from django.conf.urls import url

from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
]
