from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<dataset_name>[a-zA-Z0-9-_.]+)/$', views.datasets, name='datasets'),
    url(r'', views.annotations, name='annotations'),
]
