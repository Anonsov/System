from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  
    solved_count = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
