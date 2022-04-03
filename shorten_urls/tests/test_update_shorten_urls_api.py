import pytest

from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403

from shorten_urls.models import ShortenURL


def test_update_shorten_url_superuser(
    client,
    django_db_setup,
    get_superuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )
    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    data = resp.json()
    data = ShortenURL.objects.get(id=data["id"])
    assert data.url == "https://samsulhadi.com"
    assert data.created_by == superuser
    assert resp.status_code == 200

    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_staffuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )
    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    data = resp.json()
    data = ShortenURL.objects.get(id=data["id"])
    assert data.url == "https://samsulhadi.com"
    assert data.created_by == staff_user
    assert resp.status_code == 200


def test_update_shorten_url_staffuser(
    client,
    django_db_setup,
    get_staffuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )
    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    data = resp.json()
    assert data["detail"] == "Not found."
    assert resp.status_code == 404

    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_staffuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )
    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    data = resp.json()
    data = ShortenURL.objects.get(id=data["id"])
    assert data.url == "https://samsulhadi.com"
    assert data.created_by == staff_user
    assert resp.status_code == 200


def test_update_shorten_url_wrong_token(
    client, django_db_setup, create_shorten_url_by_superuser
):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

    resp = client.put(
        uri,
        data={},
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Given token not valid for any token type"


def test_update_shorten_url_no_token(
    client, django_db_setup, create_shorten_url_by_superuser
):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = ""
    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Authentication credentials were not provided."


def test_update_shorten_url_superuser_empty_payload(
    client, django_db_setup, get_superuser_token, create_shorten_url_by_superuser
):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.put(
        uri,
        data={},
        content_type="application/json",
    )
    assert resp.json()["url"][0] == "This field is required."
    assert resp.status_code == 400


@pytest.mark.parametrize(
    "client, url, error, get_superuser_token, django_db_setup, create_shorten_url_by_superuser",
    [
        ("", None, "This field may not be null.", "", "", ""),
        ("", "", "This field may not be blank.", "", "", ""),
        ("", "wrong", "Enter a valid URL.", "", "", ""),
    ],
    indirect=[
        "client",
        "get_superuser_token",
        "django_db_setup",
        "create_shorten_url_by_superuser",
    ],
)
def test_update_shorten_url_superuser_invalid_payload(
    client,
    url,
    error,
    get_superuser_token,
    django_db_setup,
    create_shorten_url_by_superuser,
):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )
    total = ShortenURL.objects.count()
    resp = client.put(
        uri,
        data={"url": url},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json()["url"][0] == error
    assert ShortenURL.objects.count() == total


def test_update_a_shorten_url_404(
    client,
    django_db_setup,
    get_superuser_token,
    create_shorten_url_by_superuser,
):
    user, staff_user, superuser = django_db_setup
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": 1000},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.put(
        uri,
        data={"url": "https://samsulhadi.com"},
        content_type="application/json",
    )
    data = resp.json()
    assert data["detail"] == "Not found."
    assert resp.status_code == 404
