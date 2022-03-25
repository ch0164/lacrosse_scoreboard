from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_scorekeeper = models.BooleanField(default=False)