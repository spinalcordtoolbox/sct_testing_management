from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Acquisition
from .serializers import AcquisitionSerializer


def _get_datasets(request):
    params = {}
    queryset = Acquisition.objects.all()
    params['images__pam50'] = request.GET.get('pam50')
    params['images__ms_mapping'] = request.GET.get('ms_mapping')
    params['images__gm_model'] = request.GET.get('gm_model')
    params['images__contrast'] = request.GET.get('contrast')
    params['demographic__pathology'] = request.GET.get('pathology')
    params['images__labeled_images__label'] = request.GET.get('labeled')
    params = {key: value for key, value in params.items() if value}
    if params:
        queryset = queryset.filter(**params).distinct()
    ser = AcquisitionSerializer(queryset, many=True)
    return Response(ser.data)


def _post_datasets(request):
    dataset = AcquisitionSerializer(data=request.data)
    if dataset.is_valid():
        dataset.save()
        return Response(dataset.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def datasets(request):
    if request.method == 'GET':
        return _get_datasets(request)

    elif request.method == 'POST':
        return _post_datasets(request)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class Datasets(ListCreateAPIView):
    queryset = Acquisition.objects.all()
    serializer_class = AcquisitionSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_list = (
            ('pam50', 'images__pam50'),
            ('ms_mapping', 'images__ms_mapping'),
            ('gm_model', 'images__gm_model'),
            ('contrast', 'images__contrast'),
            ('pathology', 'demographic__pathology'),
            ('label', 'images__labeled_images__label')
        )
        filters = {}
        for param, filter_ in filter_list:
            if param in self.request.query_params:
                filters[filter_] = self.request.query_params[param]

        if filters:
            return queryset.filter(**filters)
        return queryset
