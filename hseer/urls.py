from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/v1/", include("usom.urls", namespace="usom_api")),
    re_path(r"^api/v1/", include("shorten_urls.urls", namespace="shorten_urls_api")),
]
