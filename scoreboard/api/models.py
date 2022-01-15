from django.db import models

from .constants import CLASS_STANDING_CHOICES, POSITION_CHOICES


# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    player_number = models.IntegerField(null = True)
    class_standing = models.CharField(max_length=2, choices=CLASS_STANDING_CHOICES, default="FR")
    major = models.CharField(max_length=100)
    position = models.CharField(max_length=4, choices=POSITION_CHOICES, default="ATT")
    hometown = models.CharField(max_length=50)
    height_feet = models.IntegerField(null=True)
    height_inches = models.IntegerField(null=True)
    weight_pounds = models.IntegerField(null=True)


class Roster(models.Model):
    team_name = models.CharField(max_length=50, default="")
    school = models.CharField(max_length=100, default="")
    coach = models.CharField(max_length=50, default="")
    player_list = models.ManyToManyField(Player, verbose_name="List of Players")
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)
