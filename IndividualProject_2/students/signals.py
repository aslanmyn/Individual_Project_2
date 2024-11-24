from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        Student.objects.create(user=instance)