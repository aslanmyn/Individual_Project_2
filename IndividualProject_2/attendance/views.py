from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsAdminOrTeacher, IsStudentOrReadOnly

class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'teacher':
            return Attendance.objects.filter(course__instructor=user)
        elif user.role == 'student':
            return Attendance.objects.filter(student=user)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'teacher':
            raise PermissionDenied("Only teachers can mark attendance.")
        serializer.save()

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsStudentOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'teacher':
            return Attendance.objects.filter(course__instructor=user)
        elif user.role == 'student':
            return Attendance.objects.filter(student=user)
        return Attendance.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        attendance = self.get_object()
        if user.role != 'teacher' or attendance.course.instructor != user:
            raise PermissionDenied("Only the course instructor can update attendance.")
        serializer.save()