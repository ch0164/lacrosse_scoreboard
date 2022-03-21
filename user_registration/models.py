from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_scorekeeper = models.BooleanField(default=False)