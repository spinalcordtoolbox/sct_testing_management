from test_plus.test import TestCase

from ..models import Acquisition

from . import factories


def dummy(*args):
    return True


class TestSubject(TestCase):
    def setUp(self):
        acq = factories.AcquisitionFactory()
        demo = factories.DemographicFactory(acquisition=acq)

    def test_default_dict(self):
        subject = Acquisition.objects.all()[0]
        # assert str(subject) == 'center-0_study-0_subject-0'
        # sub_dict = subject.to_dict()
        # self.assertTrue(subject.to_dict()['study'])
        # self.assertTrue(subject.to_dict()['subject'])
