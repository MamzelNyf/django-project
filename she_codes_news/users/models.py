from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL
from PIL import Image



class CustomUser(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # run the save method from the parents
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,  300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
