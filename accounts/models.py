from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('organization', 'Organization'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )

    location = models.CharField(max_length=255, blank=True)