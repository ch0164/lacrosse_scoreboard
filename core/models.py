from pyexpat import model
from tkinter import CASCADE
from django.db import models

from .constants import CLASS_STANDING_CHOICES, POSITION_CHOICES


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")


class Coach(models.Model):
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")


class Player(models.Model):
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    player_number = models.IntegerField("Uniform Number", null = True)
    class_standing = models.CharField("Class", max_length=2, choices=CLASS_STANDING_CHOICES, default="FR")
    major = models.CharField("Major", max_length=100)
    position = models.CharField("Position", max_length=4, choices=POSITION_CHOICES, default="ATT")
    hometown = models.CharField("Hometown", max_length=50)
    height_feet = models.IntegerField("Height (feet)", null=True)
    height_inches = models.IntegerField("Height (inches)", null=True)
    weight_pounds = models.IntegerField("Weight (pounds)", null=True)
    #coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (#{self.player_number}) "


class Roster(models.Model):
    team_name = models.CharField(max_length=50, default="")
    school = models.CharField(max_length=100, default="")
    #coach = models.OneToOneField(Coach, on_delete=models.CASCADE)
    coach = models.CharField(max_length=100, default="")
    player_list = models.ManyToManyField(Player, verbose_name="List of Players")
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_name}"


class Scorebook(models.Model):
    pass
