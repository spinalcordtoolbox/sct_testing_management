from rest_framework import serializers

from . import models


class LabeledImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LabeledImage
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    labeled_images = LabeledImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Image
        fields = '__all__'


class DemographicSerialer(serializers.ModelSerializer):

    class Meta:
        model = models.Demographic
        fields = '__all__'


class AcquisitionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    demographic = DemographicSerialer(many=False, read_only=True)

    class Meta:
        model = models.Acquisition
        fields = '__all__'
