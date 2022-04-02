from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from shorten_urls.models import ShortenURL
from shorten_urls.serializers import ShortenURLSerializer


class ShortenURLViewSet(viewsets.ModelViewSet):
    serializer_class = ShortenURLSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return ShortenURL.objects.filter(created_by=self.request.user)
        else:
            return ShortenURL.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
