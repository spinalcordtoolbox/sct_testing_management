from test_plus.test import TestCase
from unittest import mock

from . import factories
from .. import models


class TestSubject(TestCase):
    def setUp(self):
        self.acq = factories.AcquisitionFactory()
        factories.DemographicFactory(acquisition=self.acq)
        self.mock_image = mock.MagicMock()

    def test_default_dict(self):
        subject = models.Acquisition.objects.all()[0]
        assert subject.id

    def test_valid_image(self):
        models.nib.load = self.mock_image
        obj = models.Image()
        obj.contrast = 't2'
        obj.filename = '/path/to/img.nii.gz'

        img = obj.validate_filename()
        assert img
        self.mock_image.assert_called()

    def test_save_image(self):
        def get_zooms():
            return (1, 1, 1)

        models.nib.load = self.mock_image
        models.nib.load.header.get_zooms.side_effect = lambda x: (1,1,1)
        image = models.Image(filename='path/to/t2.nii.gz',
                             contrast='t2',
                             acquisition=self.acq)
        image.save()

        assert image.filestate == models.Image.OK_FILE[0]
        self.mock_image.assert_called()
        # self.mock_image.header.get_zooms.assert_called()
        # assert image.resolution == '1.0x1.0x1.0'

    def test_invalid_image(self):
        models.nib.load = mock.MagicMock(side_effect=Exception)
        image = models.Image(filename='invalid/to/t2.nii.gz',
                             contrast='t2',
                             acquisition=self.acq)
        image.save()

        assert image.filestate == models.Image.ERR_FILE[0]
