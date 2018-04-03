from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from test_plus.test import TestCase

from .. import serializers
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
        factories.ImageFactory(acquisition=acq, contrast='t1', pam50=False)
        factories.ImageFactory(acquisition=acq, contrast='t2', pam50=False)
        factories.ImageFactory(acquisition=acq, contrast='mt', pam50=True)

        user = factories.UserFactory(username='test-admin')
        user.set_password('secret')
        user.save()


    def test_refuse_non_authicated_requests(self):
        self.client.logout()
        url = reverse('annotations:api-datasets')
        response = self.client.get(url)
        assert response.status_code == 403

        response = self.client.post(url)
        assert response.status_code == 403

        response = self.client.put(url)
        assert response.status_code == 403

    def test_get_all_datasets(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(reverse('annotations:api-datasets'))
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_get_pam50(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(reverse('annotations:api-datasets'), {'pam50': True})
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_get_t2(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(
            reverse('annotations:api-datasets'), {'contrast': 't2'}
        )
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_post_empty_dataset(self):
        data = {'demographic': {}, 'images': []}
        self.client.login(username='test-admin', password='secret')
        response = self.client.post(
            reverse('annotations:api-datasets'), data=data, format='json'
        )
        assert response.status_code == 400

    def test_post_minimal_dataset(self):
        data = {
            'center': 'c1001',
            'scanner': 's1001',
            'session': 'ses1001',
            'study': 'study1001'
        }
        self.client.login(username='test-admin', password='secret')
        response = self.client.post(
            reverse('annotations:api-datasets'), data=data, format='json'
        )
        assert response.status_code == 201
