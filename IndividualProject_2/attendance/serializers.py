from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status', 'remarks', 'student_email', 'course_name']
        read_only_fields = ['id', 'student_email', 'course_name']

    def validate_date(self, value):
        from django.utils.timezone import now
        if value > now().date():
            raise serializers.ValidationError("Attendance date cannot be in the future.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if user.role not in ['teacher', 'admin']:
            raise serializers.ValidationError("Only teachers or admins can manage attendance.")
        return data