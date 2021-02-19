from django.test import TestCase
from django.test.client import RequestFactory
from services.views import download_bundle

class DownloadTest(TestCase):
    def setup(self):
        self.factory = RequestFactory()

    def test_details(self):
        request = self.factory.get('/services/download/3')
        response = download_bundle(request,3)
        self.assertEqual(response.status_code, 200)
