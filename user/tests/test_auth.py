from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


token_url = reverse('token_obtain_pair')
refresh_url = reverse('token_refresh')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the Authentication features of the Token API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test generates JWT token for valid credentials"""

        user_details = {
            'first_name': 'Test f_name',
            'last_name': 'Test l_name',
            'email': 'test@example.com',
            'password': 'testpythonuserpassword123',
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(token_url, payload)

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""

        create_user(
            email='test@example.com',
            password='goodpass'
        )

        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }

        res = self.client.post(token_url, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""

        payload = {
            'email': 'test@example.com',
            'password': ''
        }

        res = self.client.post(token_url, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_generates_new_access_token(self):
        """Test that refresh token returns a new access token"""

        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(token_url, payload)

        refresh_token = res.data['refresh']

        refresh_payload = {
            'refresh': refresh_token
        }

        res = self.client.post(refresh_url, refresh_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

        def test_refresh_token_invalid(self):
            """Test refresh token fails if invalid"""

            payload = {
                'refresh': 'invalidtoken'
            }

            res = self.client.post(refresh_url, payload)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
