from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    full_name = models.CharField(max_length=255)
    dob = models.DateField("Date of Birth", null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"