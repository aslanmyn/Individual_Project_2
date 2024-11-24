from rest_framework import viewsets, permissions
from django.core.cache import cache
from django.conf import settings
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrOwner
from utils.cache_analysis import log_cache_hit_or_miss

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"students_{user.id}"
        cached_students = cache.get(cache_key)
        log_cache_hit_or_miss(cache_key, cached_students)

        if not cached_students:
            if user.role == 'admin':
                cached_students = self.queryset
            elif user.role == 'student':
                cached_students = self.queryset.filter(user=user)
            else:
                cached_students = Student.objects.none()

            cache.set(cache_key, cached_students, timeout=CACHE_TTL)

        return cached_students

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f"students_{self.request.user.id}")  