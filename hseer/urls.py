from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', include("sbadmin2.urls")),
    path("admin/", admin.site.urls),
]
