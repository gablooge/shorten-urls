import pytest

from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403

from shorten_urls.models import ShortenURL


def test_create_shorten_url_superuser(client, django_db_setup, get_superuser_token):
    user, staff_user, superuser = django_db_setup
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )
    total = ShortenURL.objects.count()
    resp = client.post(
        uri,
        data={
            "url": "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
        },
        content_type="application/json",
    )
    data = resp.json()
    assert (
        data["url"]
        == "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
    )
    assert len(data["shorten"]) == 25  # BASE_URL + MAXIMUM_URL_CHARS
    assert resp.status_code == 201
    assert ShortenURL.objects.count() == total + 1
    assert ShortenURL.objects.get(id=data["id"]).created_by == superuser


def test_create_shorten_url_staffuser(client, django_db_setup, get_staffuser_token):
    user, staff_user, superuser = django_db_setup
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )
    total = ShortenURL.objects.count()
    resp = client.post(
        uri,
        data={
            "url": "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
        },
        content_type="application/json",
    )
    data = resp.json()
    assert (
        data["url"]
        == "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
    )
    assert len(data["shorten"]) == 25  # BASE_URL + MAXIMUM_URL_CHARS
    assert resp.status_code == 201
    assert ShortenURL.objects.count() == total + 1
    assert ShortenURL.objects.get(id=data["id"]).created_by == staff_user


def test_create_shorten_url_wrong_token(client, django_db_setup):
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

    resp = client.post(
        uri,
        data={},
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Given token not valid for any token type"


def test_create_shorten_url_no_token(client, django_db_setup):
    uri = reverse("shorten_urls_api:ShortenURL-list")

    resp = client.post(
        uri,
        data={},
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Authentication credentials were not provided."


def test_create_shorten_url_superuser_empty_payload(
    client, django_db_setup, get_superuser_token
):
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.post(
        uri,
        data={},
        content_type="application/json",
    )
    assert resp.json()["url"][0] == "This field is required."
    assert resp.status_code == 400


@pytest.mark.parametrize(
    "client, url, error, get_superuser_token, django_db_setup",
    [
        ("", None, "This field may not be null.", "", ""),
        ("", "", "This field may not be blank.", "", ""),
        ("", "wrong", "Enter a valid URL.", "", ""),
    ],
    indirect=["client", "get_superuser_token", "django_db_setup"],
)
def test_create_shorten_url_superuser_invalid_payload(
    client, url, error, get_superuser_token, django_db_setup
):
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )
    total = ShortenURL.objects.count()
    resp = client.post(
        uri,
        data={"url": url},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json()["url"][0] == error
    assert ShortenURL.objects.count() == total
