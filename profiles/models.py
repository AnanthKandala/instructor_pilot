from django.db import models
from django.contrib.auth.models import User
from students.models import Student
# from django.core.validators import MinLengthValidator

# Create your models here.
class BaseProfile(models.Model):
    avatar = models.ImageField(
        upload_to='avatars/',
        default="no_avatar.png"
    )

    bio = models.TextField(
        max_length=500,
        default = "No bio ..."
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return f"Profile {self.id}"

    class Meta:
        abstract = True


class UserProfile(BaseProfile):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        )
    

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"Profile of User {self.user.username} ({self.user.first_name} {self.user.last_name})"
        else:
            return f"Profile of User {self.user.username}"
    @classmethod
    def create_from_canvas_user(cls, canvas_user_id):
        raise NotImplementedError
        

class StudentProfile(BaseProfile):
    student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        )
    
    def __str__(self):
        return f"Profile of student {self.student.first_name} {self.student.last_name} ({self.student.uni_id})"

    @classmethod
    def create_from_canvas_user(cls, canvas_user_id):
        raise NotImplementedError

    
