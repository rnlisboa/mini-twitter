from django.db import models
from django.contrib.auth.models import User

def upload_image(instance, filename):
    return f'images/profiles/{instance}-{filename}'

class ProfileUserModel(models.Model):
    photo = models.ImageField(
        null=True, blank=True, upload_to=upload_image, default=''
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class UserPostModel(models.Model):
    twitt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        null=True, blank=True, upload_to=upload_image, default=''
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário'
    )

class FollowModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True)
