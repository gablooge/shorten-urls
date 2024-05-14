from django.conf import settings
from django.db import models

from shorten_urls.utils import create_shortened_url


class ShortenURL(models.Model):
    url = models.URLField(max_length=255)
    shorten = models.URLField(max_length=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified"]

    def save(self, *args, **kwargs):
        if not self.shorten:
            self.shorten = settings.SHORTEN_BASE_URL + "/" + create_shortened_url(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.id, self.shorten)
