from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^v1/api/datasets/$', views.Datasets.as_view(), name='api-datasets'),
    url(r'^v1/api/images/$', views.Images.as_view(), name='api-images'),
    url(r'^v1/api/labeledimages/$', views.LabeledImages.as_view(), name='api-labeledimages'),
    url(r'^v1/api/demographics/$', views.Demographics.as_view(), name='api-demographics'),
]
