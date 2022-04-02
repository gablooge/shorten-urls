from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403


def test_create_shorten_url_super_user(client, django_db_setup, get_superuser_token):
    uri = reverse("shorten_urls_api:ShortenURL-list")
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.post(
        uri,
        data={
            "url": "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
        },
        content_type="application/json",
    )
    assert (
        resp.json()["url"]
        == "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
    )
    assert len(resp.json()["shorten"]) == 25
    assert resp.status_code == 201


def test_create_shorten_url_super_user_empty_payload(
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
