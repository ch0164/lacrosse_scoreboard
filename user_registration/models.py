from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# TODO: Set user groups and permissions with below AbstractUser.
class CustomUser(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_scorekeeper = models.BooleanField(default=False)
    pass
    
    # WEBMASTER = 1
    # SCOREKEEPER = 2
    # COACH = 3
    # VISITOR = 4

    # ROLE_CHOICES = {
    #     (WEBMASTER, "Webmaster"),
    #     (SCOREKEEPER, "Scorebook Keeper"),
    #     (COACH, "Coach"),
    #     (VISITOR, "Visitor"),
    # }
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)