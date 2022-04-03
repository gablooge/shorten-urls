from rest_framework import serializers

from shorten_urls.models import ShortenURL


class ShortenURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenURL
        fields = ("id", "url", "shorten", "created", "modified")
        read_only_fields = ("id", "shorten", "created", "modified", "created_by")


class ShortenURLSuperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenURL
        fields = ("id", "url", "shorten", "created", "modified", "created_by")
        read_only_fields = ("id", "shorten", "created", "modified", "created_by")
