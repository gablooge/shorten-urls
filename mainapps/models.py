from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from solo.models import SingletonModel

User = get_user_model()

STATUS = ((1, "ACTIVE"), (2, "DRAFT"), (3, "VERIFIED"), (4, "REJECTED"), (5, "QUEUE"))


class BaseAppModel(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_create_by_user",
        verbose_name="Dibuat Oleh",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=2)

    class Meta:
        abstract = True


class TemplateConfig(SingletonModel):
    site_name = models.CharField(max_length=50, default=settings.DEFAULT_SITE_NAME)
    logo = models.ImageField("Logo", upload_to="logo/", null=True, blank=True)
    manual_book = models.URLField("Link Manual Book", blank=True, null=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name = "Site Configuration"
