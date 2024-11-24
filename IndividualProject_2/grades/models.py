from django.db import models
from django.conf import settings
from courses.models import Course

class Grade(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='grades'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='given_grades'
    )

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.email} - {self.course.name}: {self.grade}"