from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403

from shorten_urls.models import ShortenURL


# region delete single
def test_delete_a_shorten_url_superuser(
    client,
    django_db_setup,
    get_superuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    total = ShortenURL.objects.count()
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.delete(
        uri,
        content_type="application/json",
    )
    assert ShortenURL.objects.count() == total - 1
    assert resp.status_code == 204

    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_staffuser["id"]},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.delete(
        uri,
        content_type="application/json",
    )
    assert ShortenURL.objects.count() == total - 2
    assert resp.status_code == 204


def test_delete_a_shorten_url_staffuser(
    client,
    django_db_setup,
    get_staffuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    total = ShortenURL.objects.count()
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_superuser["id"]},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )

    resp = client.delete(
        uri,
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

    resp = client.delete(
        uri,
        content_type="application/json",
    )
    assert ShortenURL.objects.count() == total - 1
    assert resp.status_code == 204


def test_delete_a_shorten_url_wrong_token(client, django_db_setup):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": 1},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

    resp = client.delete(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Given token not valid for any token type"


def test_delete_a_shorten_url_no_token(client, django_db_setup):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": 1},
    )
    resp = client.delete(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Authentication credentials were not provided."


def test_delete_a_shorten_url_404(
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

    resp = client.delete(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert data["detail"] == "Not found."
    assert resp.status_code == 404


# endregion
