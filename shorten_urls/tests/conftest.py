import pytest
from django.urls import reverse


@pytest.fixture(scope="function")
def create_shorten_url_by_superuser(client, django_db_setup, get_superuser_token):
    user, staff_user, superuser = django_db_setup
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

    return resp.json()


@pytest.fixture(scope="function")
def create_shorten_url_by_staffuser(client, django_db_setup, get_staffuser_token):
    user, staff_user, superuser = django_db_setup
    uri = reverse("shorten_urls_api:ShortenURL-list")

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )

    resp = client.post(
        uri,
        data={
            "url": "https://www.highsnobiety.com/p/louis-vuitton-basketball-sneakers/"
        },
        content_type="application/json",
    )

    return resp.json()
