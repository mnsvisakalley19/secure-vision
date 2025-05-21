from django.db import models
from django.contrib.auth.models import User



class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='user_faces/')


    def __str__(self):
        return self.user.username

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
    
    class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
