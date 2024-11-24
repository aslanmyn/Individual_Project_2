from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'dob', 'registration_date')
    search_fields = ('full_name', 'user__email')