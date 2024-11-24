from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsTeacherOrAdmin, IsStudentOrAdmin


class GradeListCreateView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Grade.objects.all()  
        elif user.role == 'teacher':
            return Grade.objects.filter(teacher=user) 
        elif user.role == 'student':
            return Grade.objects.filter(student=user)  
        return Grade.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "teacher":
            raise PermissionDenied("Only teachers can assign grades.")
        
        grade_value = self.request.data.get("grade")
        if grade_value is None:
            raise ValidationError({"grade": "Grade is required."})
        try:
            grade_value = float(grade_value)
            if grade_value <= 0:
                raise ValidationError({"grade": "Grade must be a positive number."})
        except ValueError:
            raise ValidationError({"grade": "Grade must be a valid number."})

        serializer.save(teacher=user)


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsStudentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Grade.objects.all()  
        elif user.role == 'teacher':
            return Grade.objects.filter(teacher=user) 
        elif user.role == 'student':
            return Grade.objects.filter(student=user)
        return Grade.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        grade = self.get_object()
        if user.role != 'teacher' or grade.teacher != user:
            raise PermissionDenied("Only the teacher who assigned this grade can update it.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'admin':
            raise PermissionDenied("Only administrators can delete grades.")
        instance.delete()