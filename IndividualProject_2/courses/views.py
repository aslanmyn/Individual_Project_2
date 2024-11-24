from rest_framework import viewsets, permissions
from django.core.cache import cache
from django.conf import settings
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from utils.cache_analysis import log_cache_hit_or_miss

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"courses_{user.id}"
        cached_courses = cache.get(cache_key)
        log_cache_hit_or_miss(cache_key, cached_courses)

        if not cached_courses:
            if user.role == 'admin':
                cached_courses = self.queryset
            elif user.role == 'teacher':
                cached_courses = self.queryset.filter(instructor=user)
            elif user.role == 'student':
                cached_courses = self.queryset
            else:
                cached_courses = Course.objects.none()

            cache.set(cache_key, cached_courses, timeout=CACHE_TTL)

        return cached_courses

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'teacher':
            raise PermissionError("Only teachers can create courses.")
        serializer.save(instructor=user)
        cache.delete(f"courses_{user.id}")  

    def perform_update(self, serializer):
        user = self.request.user
        course = self.get_object()
        if user.role != 'teacher' or course.instructor != user:
            raise PermissionError("Only the instructor can update this course.")
        serializer.save()
        cache.delete(f"courses_{user.id}")  


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"enrollments_{user.id}"
        cached_enrollments = cache.get(cache_key)
        log_cache_hit_or_miss(cache_key, cached_enrollments)

        if not cached_enrollments:
            if user.role == 'admin':
                cached_enrollments = self.queryset
            else:
                cached_enrollments = Enrollment.objects.none()

            cache.set(cache_key, cached_enrollments, timeout=CACHE_TTL)

        return cached_enrollments