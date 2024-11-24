from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'teacher']

class IsStudentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'student'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.student == request.user