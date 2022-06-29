from django.contrib.auth.models import User
from students.models import Student
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, StudentProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.update_or_create(user=instance)

@receiver(post_save, sender=Student)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    StudentProfile.objects.update_or_create(student=instance)