from unittest.mock import patch

from test_plus.test import TestCase

from . import factories
from .. import models


class TestSubject(TestCase):
    def setUp(self):
        self.acq = factories.AcquisitionFactory()
        factories.DemographicFactory(acquisition=self.acq)

    def test_default_dict(self):
        subject = models.Acquisition.objects.all()[0]
        assert subject.id

    @patch('nibabel.load', first=True)
    def test_save_image(self, mock_load):
        image = models.Image(filename='path/to/t2.nii.gz',
                             contrast='t2',
                             acquisition=self.acq)
        image.save()

        assert image.filestate == models.Image.OK_FILE[0]

    @patch('nibabel.load', side_effect=Exception)
    def test_invalid_image(self, mock_load):
        image = models.Image(filename='invalid/to/t2.nii.gz',
                             contrast='t2',
                             acquisition=self.acq)
        image.save()

        assert image.filestate == models.Image.ERR_FILE[0]
