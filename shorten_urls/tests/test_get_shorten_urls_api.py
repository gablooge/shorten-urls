from django.urls import reverse

from usom.tests.conftest import *  # noqa: F401, F403

from shorten_urls.models import ShortenURL


# region get list
def test_get_list_shorten_url_superuser(
    client,
    django_db_setup,
    get_superuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    uri = reverse("shorten_urls_api:ShortenURL-list")

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert len(data) == ShortenURL.objects.count()
    assert "created_by" in data[0]
    assert resp.status_code == 200


def test_get_list_shorten_url_staffuser(
    client,
    django_db_setup,
    get_staffuser_token,
    create_shorten_url_by_superuser,
    create_shorten_url_by_staffuser,
):
    user, staff_user, superuser = django_db_setup
    uri = reverse("shorten_urls_api:ShortenURL-list")

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_staffuser_token["access"]
    )

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert len(data) == ShortenURL.objects.count() - 1
    assert data[0]["shorten"] == create_shorten_url_by_staffuser["shorten"]
    assert "created_by" not in data[0]
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


# endregion

# region get single
def test_get_a_shorten_url_superuser(
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

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert data["created_by"] == superuser.id
    assert data["shorten"] == create_shorten_url_by_superuser["shorten"]
    assert resp.status_code == 200

    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": create_shorten_url_by_staffuser["id"]},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer {}".format(
        get_superuser_token["access"]
    )

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert data["created_by"] == staff_user.id
    assert data["shorten"] == create_shorten_url_by_staffuser["shorten"]
    assert resp.status_code == 200


def test_get_a_shorten_url_staffuser(
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

    resp = client.get(
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

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert "created_by" not in data
    assert data["shorten"] == create_shorten_url_by_staffuser["shorten"]
    assert resp.status_code == 200


def test_get_a_shorten_url_wrong_token(client, django_db_setup):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": 1},
    )

    client.defaults["HTTP_AUTHORIZATION"] = "Bearer wrong"

    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Given token not valid for any token type"


def test_get_a_shorten_url_no_token(client, django_db_setup):
    uri = reverse(
        "shorten_urls_api:ShortenURL-detail",
        kwargs={"pk": 1},
    )
    resp = client.get(
        uri,
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Authentication credentials were not provided."


def test_get_a_shorten_url_404(
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

    resp = client.get(
        uri,
        content_type="application/json",
    )
    data = resp.json()
    assert data["detail"] == "Not found."
    assert resp.status_code == 404


# endregion
