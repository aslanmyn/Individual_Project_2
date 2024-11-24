from rest_framework.permissions import BasePermission

class IsRecipientOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.recipient == request.user