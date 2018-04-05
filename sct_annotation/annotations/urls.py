from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^v1/api/datasets/$', views.Datasets.as_view(), name='api-datasets'),
]
