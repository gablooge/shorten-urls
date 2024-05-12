from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APIClient

from shorten_urls.models import ShortenURL
from usom.models import User


class ShortenURLViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username="test_superuser",
            password=settings.TEST_PASSWORD,
        )

        self.user = User.objects.create_user(
            username="testuser", password=settings.TEST_PASSWORD
        )

    def test_create_shorten_url_by_superuser(self):
        url_data = {"url": "http://example.com"}
        url = reverse("shorten_urls_api:shorten_url-list")
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, url_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("shorten", response.data)
        self.assertIn("created_by", response.data)

        # Check if the ShortenURL object was created in the database
        shorten_url = ShortenURL.objects.first()
        self.assertIsNotNone(shorten_url)
        self.assertEqual(shorten_url.url, url_data["url"])
        self.assertEqual(shorten_url.created_by, self.superuser)

    def test_create_shorten_url_by_user(self):
        url_data = {"url": "http://example.com"}
        url = reverse("shorten_urls_api:shorten_url-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, url_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("shorten", response.data)
        self.assertNotIn("created_by", response.data)

        # Check if the ShortenURL object was created in the database
        shorten_url = ShortenURL.objects.first()
        self.assertIsNotNone(shorten_url)
        self.assertEqual(shorten_url.url, url_data["url"])
        self.assertEqual(shorten_url.created_by, self.user)

    def test_create_shorten_url_wrong_token(self):
        url_data = {"url": "http://example.com"}
        wrong_token = "wrongtoken"
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {wrong_token}")
        url = reverse("shorten_urls_api:shorten_url-list")
        response = self.client.post(url, url_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(ShortenURL.objects.exists())

    @parameterized.expand(
        [
            ("", "This field may not be blank."),
            ("invalid-url", "Enter a valid URL."),
        ]
    )
    def test_create_shorten_url_invalid_input(self, url, error_message):
        url_data = {"url": url}
        self.client.force_authenticate(user=self.user)
        url = reverse("shorten_urls_api:shorten_url-list")
        response = self.client.post(url, url_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["url"][0], error_message)
        self.assertFalse(ShortenURL.objects.exists())

    def test_retrieve_shorten_url_by_superuser(self):
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.superuser
        )
        url = reverse("shorten_urls_api:shorten_url-detail", args=[shorten_url.id])
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], shorten_url.id)
        self.assertEqual(response.data["url"], shorten_url.url)
        self.assertIn("shorten", response.data)
        self.assertIn("created_by", response.data)

    def test_retrieve_shorten_url_by_user(self):
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )
        url = reverse("shorten_urls_api:shorten_url-detail", args=[shorten_url.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], shorten_url.id)
        self.assertEqual(response.data["url"], shorten_url.url)
        self.assertIn("shorten", response.data)
        self.assertNotIn("created_by", response.data)

    def test_retrieve_a_shorten_url_404(self):
        # Create a ShortenURL
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )

        # Try to retrieve the ShortenURL with a non-existing ID
        non_existing_id = shorten_url.id + 100  # Assuming this ID doesn't exist
        url = reverse("shorten_urls_api:shorten_url-detail", args=[non_existing_id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_shorten_urls(self):
        ShortenURL.objects.create(url="http://example1.com", created_by=self.user)
        ShortenURL.objects.create(url="http://example2.com", created_by=self.user)
        url = reverse("shorten_urls_api:shorten_url-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_shorten_url(self):
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )
        new_url = "http://newexample.com"
        data = {"url": new_url}
        url = reverse("shorten_urls_api:shorten_url-detail", args=[shorten_url.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url"], new_url)

        # Check if the ShortenURL object was updated in the database
        shorten_url.refresh_from_db()
        self.assertEqual(shorten_url.url, new_url)

    @parameterized.expand(
        [
            ("", "This field may not be blank."),
            ("invalid-url", "Enter a valid URL."),
        ]
    )
    def test_update_shorten_url_invalid_input(self, new_url, error_message):
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )
        data = {"url": new_url}
        url = reverse("shorten_urls_api:shorten_url-detail", args=[shorten_url.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["url"][0], error_message)

        # Check if the ShortenURL object was updated in the database
        shorten_url.refresh_from_db()
        self.assertNotEqual(shorten_url.url, new_url)

    def test_update_a_shorten_url_404(self):
        # Create a ShortenURL
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )

        # Try to update the ShortenURL with a non-existing ID
        non_existing_id = shorten_url.id + 100  # Assuming this ID doesn't exist
        url = reverse("shorten_urls_api:shorten_url-detail", args=[non_existing_id])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            url,
            data={"url": "https://samsulhadi.com"},
            content_type="application/json",
        )

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shorten_url(self):
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )
        url = reverse("shorten_urls_api:shorten_url-detail", args=[shorten_url.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShortenURL.objects.filter(id=shorten_url.id).exists())

    def test_delete_a_shorten_url_404(self):
        # Create a ShortenURL
        shorten_url = ShortenURL.objects.create(
            url="http://example.com", created_by=self.user
        )

        # Try to delete the ShortenURL with a non-existing ID
        non_existing_id = shorten_url.id + 100  # Assuming this ID doesn't exist
        url = reverse("shorten_urls_api:shorten_url-detail", args=[non_existing_id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
