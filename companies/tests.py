from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Company

User = get_user_model()


class CompanyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_create_company(self):
        url = '/api/v1/companies/'
        data = {
            'name': 'wanted',
            'country': 'Republic Korea',
            'location': 'Busan',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'wanted')

    def test_list_companies(self):
        url = '/api/v1/companies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

