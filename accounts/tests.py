from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import Account, Operation
from users.models import User
from accounts.forms import ActivateSavingForm, SendMoneyForm, LocalMoneyForm
from django.contrib.auth.hashers import make_password



class AccountViewSetTests(TestCase):
    def setUp(self):
        # Set up test data if needed
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create(email=self.user_data['email'], password=make_password(self.user_data['password']))
        self.user.bank_account.balance = 10000
        self.user.saving_account.balance = 10000
        self.user.bank_account.save()
        self.user.saving_account.save()
        self.bank_account = self.user.bank_account
        self.saving_account = self.user.saving_account

        target_user = User.objects.create(email="target@example.com", password=make_password("testpassword"))
        self.target_account = target_user.bank_account
        self.client = APIClient()

    def get_access_key(self):
        key_url = reverse("users:users-code")
        self.client.post(key_url, data=self.user_data)
        return User.objects.get(email=self.user.email).access_key
        
    def test_list_accounts(self):
        # Test the list endpoint
        url = reverse("accounts:accounts-list")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response=response, template_name="accounts.html")

    def test_activate_account(self):
        # Test the activate_account endpoint
        url = reverse("accounts:accounts-activate-account")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"saving_percent": 10}
        response = self.client.post(url, data=data)
        updated_user = User.objects.get(email=self.user.email)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful activation
        self.assertTrue(updated_user.saving_account.is_activated)
        self.assertEqual(updated_user.saving_account.saving_percent, 10)
        

    def test_put_money(self):
        # Test the put_money endpoint
        access_key = self.get_access_key()
        url = reverse("accounts:accounts-put-money")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"password": "testpassword", "access_key": access_key, "balance": 100}
        response = self.client.post(url, data=data)
        updated_user = User.objects.get(email=self.user.email)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful money transfer
        self.assertEqual(10100, updated_user.bank_account.balance)

    def test_send_money(self):
        # Test the send_money endpoint
        access_key = self.get_access_key()
        url = reverse("accounts:accounts-send-money")
        self.client.login(**self.user_data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) #test get request
        
        data = {"password": self.user_data['password'], "access_key": access_key, "balance": 50, "account_id": str(self.target_account.account_id)}
        response = self.client.post(url, data=data)
        
        self.assertTemplateNotUsed(response=response, template_name="send_money.html")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful money transfer
        updated_target = User.objects.get(email="target@example.com").bank_account
        updated_user_balance = User.objects.get(email=self.user.email).bank_account.balance
        self.assertEqual(50, updated_target.balance)
        self.assertEqual(9950, updated_user_balance)

    def test_operations(self):
        # Test the operations endpoint
        url = reverse("accounts:accounts-operations")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response=response, template_name="operations.html")

    def test_add_from_saved(self):
        # Test the add_from_saved endpoint
        access_key = self.get_access_key()
        url = reverse("accounts:accounts-add-from-saved")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"password": "testpassword", "access_key": access_key, "balance": 50}
        response = self.client.post(url, data=data)
        updated_user = User.objects.get(email=self.user)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming a redirect after successful money transfer
        self.assertEqual(10050, updated_user.bank_account.balance)
        self.assertEqual(9950, updated_user.saving_account.balance)
        

