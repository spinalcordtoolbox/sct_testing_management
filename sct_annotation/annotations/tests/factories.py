import datetime
import factory
import factory.fuzzy as fuzzy

from ..models import Acquisition, Demographic, Image


class AcquisitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Acquisition

    center = factory.Sequence(lambda n: 'center-{}'.format(n))
    study = factory.Sequence(lambda n: 'study-{}'.format(n))
    subject = factory.Sequence(lambda n: 'subject-{}'.format(n))


class DemographicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Demographic


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    contrast_category = fuzzy.FuzzyChoice(['t1', 't2', 't2s'])
    pam50 = fuzzy.FuzzyChoice([True, False])
    ms_mapping = fuzzy.FuzzyChoice([False, True])
