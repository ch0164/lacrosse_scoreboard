import uuid

from django.db import models
from django.contrib.auth.models import User

from .constants import CLASS_STANDING_CHOICES, POSITION_CHOICES
from scoreboard.settings import AUTH_USER_MODEL

# Create your models here.
class Roster(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, default="")
    school = models.CharField(max_length=100, default="")
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_name}"


class Coach(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    roster = models.OneToOneField(Roster, related_name="roster", null=True, blank=True, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.roster} -- Coach: {self.last_name}, {self.first_name}\n"

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    player_number = models.IntegerField("Player Number", null = True)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    position = models.CharField("Position", max_length=4, choices=POSITION_CHOICES, default="ATT")
    class_standing = models.CharField("Class", max_length=2, choices=CLASS_STANDING_CHOICES, default="FR")
    weight_pounds = models.IntegerField("Weight (pounds)", null=True)
    height_feet = models.IntegerField("Height (feet)", null=True)
    height_inches = models.IntegerField("Height (inches)", null=True)
    major = models.CharField("Major", max_length=100)
    hometown = models.CharField("Hometown", max_length=100)
    team = models.ForeignKey(Roster, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (#{self.player_number}) "


class Scorebook(models.Model):
    id = models.AutoField(primary_key=True)
    home_coach = models.OneToOneField(Coach, related_name="home_coach", on_delete=models.CASCADE, default=None)
    visiting_coach = models.OneToOneField(Coach, related_name="visiting_coach", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Home Team: {self.home_coach}\n" \
               f"Visiting Team: {self.visiting_coach}"
