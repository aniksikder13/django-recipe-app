from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model


# URL for manage user endpoint
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for retrieving user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            first_name= 'Test f_name',
            last_name= 'Test l_name',
        )

        self.client = APIClient()

        # force authentication
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(
            res.data,
            {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
            }
        )

    def test_post_me_not_allowed(self):
        """Test POST is not allowed on the /me endpoint"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""

        payload = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': 'newpassword123'
        }

        res = self.client.patch(ME_URL, payload)

        # refresh user from database
        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])

        self.assertTrue(
            self.user.check_password(payload['password'])
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
