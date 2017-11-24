from django.conf.urls import include, url
from django.views.static import serve
from django.conf import settings

from . import views

app_name = 'solving'
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<exercice_id>[0-9]+)/$', views.detail, name='detail'),
        url(r'^(?P<exercice_id>[0-9]+)/post_solution/$', views.postSolution, name='postSolution'),
        url(r'^(?P<solution_id>[0-9]+)/edit_solution/$', views.editSolution, name='editSolution'),
        url(r'^(?P<solution_id>[0-9]+)/delete_solution/$', views.deleteSolution, name='deleteSolution'),
        url(r'^(?P<category_id>[0-9]+)/post_exercice/$', views.postExercice, name='postExercice'),
        url(r'^(?P<exercice_id>[0-9]+)/edit_exercice/$', views.editExercice, name='editExercice'),
        url(r'^(?P<exercice_id>[0-9]+)/delete_exercice/$', views.deleteExercice, name='deleteExercice'),
        url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
        url(r'^dl/%s(?P<path>.*)$' % settings.MEDIA_URL[1:], views.protected_serve, {'document_root': settings.MEDIA_ROOT}, name='protected_serve'),
]
