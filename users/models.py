from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images", blank=True, default="default_image.jpg")
    phone = models.CharField(blank=True)