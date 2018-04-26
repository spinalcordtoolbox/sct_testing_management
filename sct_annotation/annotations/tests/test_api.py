from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from test_plus.test import TestCase

from . import factories


class TestDatasetApi(TestCase):
    """Test the REST API """

    def setUp(self):
        self.client = APIClient()
        acq = factories.AcquisitionFactory()
        acq1 = factories.AcquisitionFactory()
        factories.DemographicFactory(acquisition=acq)
        factories.DemographicFactory(acquisition=acq1)
        factories.ImageFactory(acquisition=acq, contrast='t1')
        factories.ImageFactory(acquisition=acq, contrast='t2')
        factories.ImageFactory(acquisition=acq, contrast='mt', pam50=True, is_isotropic=True, sagittal=2.0)

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

    def test_get_isotropic(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(
            reverse('annotations:api-datasets'), {'isotropic': 'True'}
        )
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_get_saggital(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(
            reverse('annotations:api-datasets'), {'sagittal': '1.0-3.0'}
        )
        assert response.status_code == 200
        assert len(response.data) == 1

        response = self.client.get(
            reverse('annotations:api-datasets'), {'sagittal': '2.0'}
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
        data = response.json()
        assert data['id']

        img = {'acquisition': data['id'], 'filename': 'path/to/img.nii.gz', 'contrast': 't2'}
        response = self.client.post(reverse('annotations:api-images'), data=img, format='json')
        data_img = response.json()
        assert response.status_code == 201
        assert data_img['id']
        assert data_img['acquisition'] == data['id']

        labeled = {'contrast': data_img['id'], 'filename': 'path/to/labeled.nii.gz', 'label': 'seg_manual'}
        response = self.client.post(reverse('annotations:api-labeledimages'), data=labeled, format='json')
        data_labeled = response.json()
        assert response.status_code == 201
        assert data_labeled['contrast'] == data_img['id']


    def test_get_image(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(reverse('annotations:api-images'), format='json')
        assert response.status_code == 200

    def test_get_labeledimages(self):
        self.client.login(username='test-admin', password='secret')
        response = self.client.get(reverse('annotations:api-labeledimages'), format='json')
        assert response.status_code == 200
