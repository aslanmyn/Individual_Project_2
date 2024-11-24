from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'grade', 'date', 'teacher')
    list_filter = ('course', 'teacher', 'date')
    search_fields = ('student__email', 'course__name', 'teacher__email')
    ordering = ('-date',)
    list_per_page = 25

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'course', 'teacher')