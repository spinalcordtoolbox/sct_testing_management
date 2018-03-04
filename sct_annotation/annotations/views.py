from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
    params['images__contrast_category'] = request.GET.get('contrast')
    params['demographic__pathology'] = request.GET.get('pathology')
    params = {key: value for key, value in params.items() if value}
    if params:
        queryset = queryset.filter(**params).distinct()
    ser = AcquisitionSerializer(queryset, many=True)
    return Response(ser.data)


def _post_datasets(request):
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
