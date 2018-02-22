from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from test_plus.test import TestCase

from .. import views
from . import factories

class TestDatasetApi(TestCase):
    """Test the REST API """

    def setUp(self):
        self.client = APIClient()
        acq = factories.AcquisitionFactory()
        acq1 = factories.AcquisitionFactory()
        factories.DemographicFactory(acquisition=acq)
        factories.DemographicFactory(acquisition=acq1)
        factories.ImageFactory(acquisition=acq)
        factories.ImageFactory(acquisition=acq)
        factories.ImageFactory(acquisition=acq)
        factories.ImageFactory(acquisition=acq)
        factories.ImageFactory(acquisition=acq)

    def test_get_all_datasets(self):
        response = self.client.get(reverse('annotations:api-datasets'))
        assert len(response.data) == 2

    def test_get_pam50(self):
        response = self.client.get(reverse('annotations:api-datasets'),
                                   {'pam50': True})
        self.assertEqual(len(response.data), 1)

    def test_get_t2(self):
        response = self.client.get(reverse('annotations:api-datasets'),
                                   {'contrast': 't2'})
        self.assertEqual(len(response.data), 1)
