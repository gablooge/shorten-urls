import pytest

from django.contrib.auth.models import User
from django.test import Client
from django.conf import settings
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.fixture(scope="function")
def client(request):
    return Client()


@pytest.fixture(scope="function")
def django_db_setup(request, db):
    """Set up database for unit test.

    Create
    - user biasa
    - superuser
    """

    user = mixer.blend(User)
    user.set_password(settings.TEST_PASSWORD)
    user.is_staff = False
    user.is_superuser = False
    user.save()

    staff_user = mixer.blend(User)
    staff_user.is_staff = True
    staff_user.is_superuser = False
    staff_user.set_password(settings.TEST_PASSWORD)
    staff_user.save()

    superuser = User.objects.create_superuser(
        username="test_superuser",
        email="test_superuser@test.com",
        password=settings.TEST_PASSWORD,
    )
    superuser.save()

    return (user, staff_user, superuser)


@pytest.fixture(scope="function")
def get_superuser_token(client, django_db_setup):
    user, staff_user, superuser = django_db_setup
    uri = reverse("usom_api:token_login")
    resp = client.post(
        uri,
        data={"username": superuser.username, "password": settings.TEST_PASSWORD},
        content_type="application/json",
    )

    return resp.json()


@pytest.fixture(scope="function")
def get_staffuser_token(client, django_db_setup):
    user, staff_user, superuser = django_db_setup
    uri = reverse("usom_api:token_login")
    resp = client.post(
        uri,
        data={"username": staff_user.username, "password": settings.TEST_PASSWORD},
        content_type="application/json",
    )

    return resp.json()
