import factory
import factory.fuzzy as fuzzy

from ..models import Acquisition, Demographic, Image
from sct_annotation.users.models import User


class AcquisitionFactory(factory.django.DjangoModelFactory):

    center = factory.Sequence(lambda n: 'center%03d' % n)
    study = factory.Sequence(lambda n: 'study%03d' % n)
    session = factory.Sequence(lambda n: 'session%03d' % n)

    class Meta:
        model = Acquisition


class DemographicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Demographic


class ImageFactory(factory.django.DjangoModelFactory):

    filename = fuzzy.FuzzyText(suffix='.nii.gz')
    pam50 = False
    sagittal = 0.0

    class Meta:
        model = Image


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
