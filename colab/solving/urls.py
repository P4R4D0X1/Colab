from django.conf.urls import url

from . import views

app_name = 'solving'
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<exercice_id>[0-9]+)/$', views.detail, name='detail'),
        url(r'^(?P<exercice_id>[0-9]+)/post_solution/$', views.postSolution, name='postSolution'),
        url(r'^(?P<solution_id>[0-9]+)/delete_solution/$', views.deleteSolution, name='deleteSolution'),
        url(r'^category/$', views.category_index, name='categoryindex'),
        url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
]
