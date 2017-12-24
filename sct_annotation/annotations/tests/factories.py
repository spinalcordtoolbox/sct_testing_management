import datetime
import factory
import factory.fuzzy as fuzzy


class AcquisitionFactory(factory.django.DjangoModelFactory):
    center = factory.Sequence(lambda n: 'center-{}'.format(n))
    study = factory.Sequence(lambda n: 'study-{}'.format(n))
    subject = factory.Sequence(lambda n: 'subject-{}'.format(n))

    class Meta:
        model = 'annotations.Acquisition'


class DemographicFactory(factory.django.DjangoModelFactory):
    subject = factory.SubFactory(AcquisitionFactory)
    nifti_path = fuzzy.FuzzyText()
    created_date = fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=datetime.timezone.utc))

    class Meta:
        model = 'annotations.Demographic'


class ImageFactory(factory.django.DjangoModelFactory):
    contrast = fuzzy.FuzzyChoice(['t1', 't2', 't2s'])
