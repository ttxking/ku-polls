from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTest(TestCase):
    """Test for authentication."""

    def setUp(self):
        """Initialize a user with username, password and first name."""
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'first_name': 'testerman'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        """If the user successfully logged out, return the 200 response code OK.

        The user first name will be show on index page.

        """
        # send login data
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get(reverse('polls:index'))
        self.assertTrue(response2.context['user'].is_authenticated)
        self.assertContains(response2, f"Welcome, {self.credentials['first_name']}")

    def test_logout(self):
        """If the user successfully logged out, return the 200 response code OK."""
        # send login data
        self.client.post(reverse('login'), self.credentials, follow=True)
        # logout
        response = self.client.post(reverse('logout'), self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertTrue(response.status_code, 200)
        # check index page
        response2 = self.client.get(reverse('polls:index'))
        self.assertFalse(response2.context['user'].is_authenticated)
        self.assertNotContains(response2, f"Welcome, {self.credentials['first_name']}")
