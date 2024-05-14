from django.urls import include, path
from rest_framework import routers

from shorten_urls.viewsets import ShortenURLViewSet

app_name = "shorten_urls_app"


class OptionalSlashRouter(routers.DefaultRouter):
    def init(self):
        super().init()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"url/shorten", ShortenURLViewSet, basename="shorten_url")

urlpatterns = [path("", include(router.urls))]
