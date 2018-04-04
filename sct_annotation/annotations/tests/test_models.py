from test_plus.test import TestCase

from ..models import Acquisition

from . import factories


class TestSubject(TestCase):
    def setUp(self):
        acq = factories.AcquisitionFactory()
        factories.DemographicFactory(acquisition=acq)

    def test_default_dict(self):
        subject = Acquisition.objects.all()[0]
        assert subject.id
