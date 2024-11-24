from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    instructor_email = serializers.EmailField(source='instructor.email', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'instructor_email']
        read_only_fields = ['id', 'instructor_email']

class EnrollmentSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'student_email', 'course_name']
        read_only_fields = ['id', 'enrollment_date', 'student_email', 'course_name']