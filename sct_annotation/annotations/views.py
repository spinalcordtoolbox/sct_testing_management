from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Acquisition
from .serializers import AcquisitionSerializer


class SCTMixin(object):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class Datasets(SCTMixin, ListCreateAPIView):

    queryset = Acquisition.objects.select_related('demographic').all().prefetch_related('images')
    serializer_class = AcquisitionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_list = (
            ('pam50', 'images__pam50'),
            ('ms_mapping', 'images__ms_mapping'),
            ('gm_model', 'images__gm_model'),
            ('contrast', 'images__contrast'),
            ('pathology', 'demographic__pathology'),
            ('label', 'images__labeled_images__label'),
            ('isotropic', 'images__is_isotropic'),
        )
        filters = {}
        for param, filter_ in filter_list:
            if param in self.request.query_params:
                filters[filter_] = self.request.query_params[param]

        for param in ['sagittal', 'corrinal', 'axial']:
            try:
                val = self.request.query_params[param]
                vals = [float(x) for x in val.split('-')]
                if len(vals) == 2:
                    filters[f'images__{param}__range'] = vals

                if len(vals) == 1:
                    filters[f'images__{param}__range'] = (vals[0] - 0.01, vals[0] + 0.01)
            except KeyError:
                pass

        if filters:
            return queryset.filter(**filters)
        return queryset
