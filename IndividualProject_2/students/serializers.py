from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'email', 'full_name', 'dob', 'registration_date']
        read_only_fields = ['id', 'user', 'email', 'registration_date']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'student':
            raise serializers.ValidationError("Only students can create a profile.")
        validated_data['user'] = user
        return super().create(validated_data)