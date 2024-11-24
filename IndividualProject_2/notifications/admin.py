from django.contrib import admin
from .models import Notification, NotificationTemplate

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'recipient_role', 'status', 'created_at', 'is_read')
    list_filter = ('recipient_role', 'status', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'message')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected notifications marked as read.")
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Selected notifications marked as unread.")
    mark_as_unread.short_description = "Mark selected as unread"