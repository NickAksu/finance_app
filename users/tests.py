from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserViewSetTestsSuccess(TestCase):
    def setUp(self):
    # Success tests
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.new_user_data = {
            "email": "testnew@example.com",
            "password": "testpassword",
        }
        self.unreal_user_data = {
            "email": "test2@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create(email=self.user_data['email'], password=make_password(self.user_data['password']))
        self.client = APIClient()

    def test_list_users(self):
        self.client.login(**self.user_data)
        url = reverse("users:users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response=response, template_name="users.html")
        
    def test_register_user(self):
        url = reverse("users:users-register")
        response = self.client.post(url, data=self.new_user_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful registration

    def test_login_user(self):
        code_url = reverse("users:users-code")
        self.client.post(code_url, data=self.user_data)
        url = reverse("users:users-login")
        access_key = int(User.objects.get(email=self.user_data['email']).access_key)
        response = self.client.post(url, data=dict(**self.user_data, access_key=access_key))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful login

    def test_create_access_code(self):
        url = reverse("users:users-code")
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #Failure test
    def test_login_user_failure(self):
        code_url = reverse("users:users-code")
        self.client.post(code_url, data=self.user_data)
        url = reverse("users:users-login")
        access_key = int(User.objects.get(email=self.user_data['email']).access_key) + 1
        response = self.client.post(url, data=dict(**self.user_data, access_key=access_key))
        self.assertEqual(response.status_code, status.HTTP_200_OK) #returns "render" with error messages generated

    def test_create_access_code_failure(self):
        url = reverse("users:users-code")
        response = self.client.post(url, data=self.unreal_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


