import unittest
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from parameterized import parameterized


@pytest.mark.django_db
class LoginTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        self.User = {
            "username": "john",
            "email": "jlennon@beatles.com",
            "password": "glass onion",
        }

        User.objects.create_user(
            username=self.User.get("username"),
            email=self.User.get("email"),
            password=self.User.get("password"),
        )

    def test_get_login_valid(self):
        # Issue a GET request.
        url = reverse("admin:login")
        response = self.client.get(url)

        self.assertTrue(response.context["user"].is_anonymous)
        self.assertEqual(response.status_code, 200)

    def test_post_login_valid(self):
        url = reverse("admin:login")

        login = self.client.login(
            username=self.User.get("username"), password=self.User.get("password")
        )
        self.assertTrue(login)
        response = self.client.post(url, self.User)

        self.assertEqual(self.User.get("username"), response.context["user"].username)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_active)

    @parameterized.expand(
        [
            ["wrong", "wrong"],  # wrong username & password
            ["", ""],  # empty credentials
        ]
    )
    def test_post_login_invalid_credentials(self, username, password):
        url = reverse("admin:login")
        user = {"username": username, "password": password}
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_anonymous)
        self.assertFalse(response.context["user"].is_active)
