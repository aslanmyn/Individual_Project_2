from rest_framework import serializers
from .models import Grade
from decimal import Decimal

class GradeSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.email', read_only=True)
    grade = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date', 'teacher', 'student_email', 'course_name', 'teacher_email']
        read_only_fields = ['id', 'date', 'teacher', 'student_email', 'course_name', 'teacher_email']

    def validate_grade(self, value):
        if value is None:
            raise serializers.ValidationError("Grade is required and cannot be null.")
        if value <= 0:
            raise serializers.ValidationError("Grade must be a positive number.")
        if value > 100:
            raise serializers.ValidationError("Grade cannot exceed 100.")
        return value
    
    def get_grade(self, obj):
        return f"{Decimal(obj.grade):.1f}"
    
    def validate(self, data):
        user = self.context['request'].user
        if user.role != 'teacher':
            raise serializers.ValidationError("Only teachers can assign grades.")
        
        if not data.get('student'):
            raise serializers.ValidationError({"student": "Student is required."})
        if not data.get('course'):
            raise serializers.ValidationError({"course": "Course is required."})
        
        return data