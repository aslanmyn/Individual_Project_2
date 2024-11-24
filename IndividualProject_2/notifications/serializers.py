from rest_framework import serializers
from .models import Notification, NotificationTemplate

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'title', 'message', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    recipient_email = serializers.EmailField(source='recipient.email', read_only=True)
    template_title = serializers.CharField(source='template.title', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_email', 'message', 'template', 'template_title',
            'recipient_role', 'created_at', 'is_read', 'status'
        ]
        read_only_fields = ['id', 'created_at', 'recipient_email', 'template_title']