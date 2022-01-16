from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# TODO: Set user groups and permissions with below AbstractUser.
# class User(AbstractUser):
#     WEBMASTER = 1
#     SCOREKEEPER = 2
#     COACH = 3
#     VISITOR = 4

#     ROLE_CHOICES = {
#         (WEBMASTER, "Webmaster"),
#         (SCOREKEEPER, "Scorebook Keeper"),
#         (COACH, "Coach"),
#         (VISITOR, "Visitor"),
#     }
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)