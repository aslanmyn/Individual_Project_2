from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.conf import settings
from .models import Notification, NotificationTemplate
from .serializers import NotificationSerializer, NotificationTemplateSerializer
from .permissions import IsRecipientOrAdmin
from utils.cache_analysis import log_cache_hit_or_miss

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)

class NotificationTemplateListView(generics.ListCreateAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipient_role', 'status', 'is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        cache_key = f"notifications_{user.id}"
        cached_notifications = cache.get(cache_key)
        log_cache_hit_or_miss(cache_key, cached_notifications)

        if not cached_notifications:
            if user.role == 'admin':
                cached_notifications = Notification.objects.all()
            else:
                cached_notifications = Notification.objects.filter(recipient=user)

            cache.set(cache_key, cached_notifications, timeout=CACHE_TTL)

        return cached_notifications

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionError("Only admins can create notifications.")
        serializer.save()
        cache.delete(f"notifications_{self.request.user.id}")  

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecipientOrAdmin]

    def get_queryset(self):
        return Notification.objects.all()