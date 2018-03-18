from django.utils.timezone import now
from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = '__all__'
        depth = 1


class DemographicSerialer(serializers.ModelSerializer):

    class Meta:
        model = models.Demographic
        fields = '__all__'
        depth = 1


class AcquisitionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    demographic = DemographicSerialer(many=False)

    class Meta:
        model = models.Acquisition
        fields = '__all__'
        depth = 1


class DatasetSerializer(serializers.Serializer):
    count = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    data = AcquisitionSerializer

    def get_count(self, obj):
        return self.instance.count()

    def get_date(self, obj):
        return now()
