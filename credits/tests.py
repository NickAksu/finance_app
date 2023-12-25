from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from credits.models import Credit
from users.models import User
from django.contrib.auth.hashers import make_password

class CreditsViewSetTests(TestCase):
    def setUp(self):
        # Set up test data if needed
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.client = APIClient()
        self.user = User.objects.create(email=self.user_data['email'], password=make_password(self.user_data['password']))
        self.client.force_login(self.user)
        
    def get_access_key(self):
        key_url = reverse("users:users-code")
        self.client.post(key_url, data=self.user_data)
        return User.objects.get(email=self.user.email).access_key

    def test_list_credits(self):
        # Test the list endpoint
        url = reverse("credits:credits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response=response, template_name="credits.html")

    def test_request_credit_get(self):
        # Test the request_credit endpoint with GET
        url = reverse("credits:credits-request-credit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response=response, template_name="request_credit.html")

    def test_request_credit_post(self):
        # Test the request_credit endpoint with POST
        access_key = self.get_access_key()
        url = reverse("credits:credits-request-credit")
        data = {
            "password": "testpassword",
            "total_sum": 1000.00,
            "persent": 5,
            "access_key": access_key,
            "period": 12,
            "is_differential": "on",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful credit request
        updated_user = User.objects.get(email=self.user.email)
        self.assertEqual(Credit.objects.count(), 1)
        self.assertEqual(updated_user.bank_account.balance, 1000)

    # Add more tests as needed
