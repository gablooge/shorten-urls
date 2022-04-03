from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403

from shorten_urls.models import ShortenURL


def test_get_list_shorten_url_superuser(
    client,
    django_db_setup,
    get_superuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    uri = reverse("shorten_urls_api:ShortenURL-list")

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert len(resp.json()) == ShortenURL.objects.count()
    assert resp.status_code == 200


def test_get_list_shorten_url_staffuser(
    client,
    django_db_setup,
    get_staffuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    uri = reverse("shorten_urls_api:ShortenURL-list")

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )

    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert len(resp.json()) == ShortenURL.objects.count() - 1
    assert resp.json()[0]["shorten"] == create_shorten_url_by_staffuser["shorten"]
    assert resp.status_code == 200


def test_get_list_shorten_url_wrong_token(client, django_db_setup):
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Given token not valid for any token type"


def test_get_list_shorten_url_no_token(client, django_db_setup):
    uri = reverse("shorten_urls_api:ShortenURL-list")

    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Authentication credentials were not provided."
