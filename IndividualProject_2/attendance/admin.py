from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'date', 'status', 'remarks')
    list_filter = ('status', 'course', 'date')
    search_fields = ('student__email', 'course__name', 'remarks')
    ordering = ('-date',)
    date_hierarchy = 'date'