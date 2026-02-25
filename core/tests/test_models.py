from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successfully(self):
        email = "test@example.com"
        password = "pass1234test"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['test3@Example.COM', 'test3@example.com'],
            ['test4@EXAMPLE.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='test1234'
            )

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises a ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='test1234'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""

        email = "test@example.com"
        password = "pass1234test"

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
