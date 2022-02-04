from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import django_tables2 as tables

from .constants import CLASS_STANDING_CHOICES, POSITION_CHOICES


# Create your models here.
class Coach(models.Model):
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")


class Roster(models.Model):
    team_name = models.CharField(max_length=50, default="")
    school = models.CharField(max_length=100, default="")
    # TODO: How many rosters should a team have?
    #coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roster", null=True)
    #coach = models.OneToOne(User, on_delete=models.CASCADE, related_name="roster", null=True)
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_name}"


class Player(models.Model):
    player_number = models.IntegerField("Player Number", null = True)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    position = models.CharField("Position", max_length=4, choices=POSITION_CHOICES, default="ATT")
    class_standing = models.CharField("Class", max_length=2, choices=CLASS_STANDING_CHOICES, default="FR")
    weight_pounds = models.IntegerField("Weight (pounds)", null=True)
    height_feet = models.IntegerField("Height (feet)", null=True)
    height_inches = models.IntegerField("Height (inches)", null=True)
    major = models.CharField("Major", max_length=100)
    hometown = models.CharField("Hometown", max_length=50)
    #team = models.ForeignKey(Roster, on_delete=models.CASCADE, default=None)
    #coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (#{self.player_number}) "


class Scorebook(models.Model):
    pass
