from django.db import models
from django.contrib.auth.models import User

from core.constants import CLASS_STANDING_CHOICES, POSITION_CHOICES, QUARTERS
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
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="coach_user", on_delete=models.CASCADE, null=True, blank=True, default=None)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    roster = models.OneToOneField(Roster, related_name="roster", null=True, blank=True, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.roster} -- Coach: {self.last_name}, {self.first_name}\n"

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    player_number = models.IntegerField("Player Number", null=True)
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


class Scorekeeper(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="scorekeeper_user", on_delete=models.CASCADE, null=True, blank=True, default=None)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")

    def __str__(self):
        return f"Scorekeeper: {self.last_name}, {self.first_name}\n"


class RunningScore(models.Model):
    id = models.AutoField(primary_key=True)
    home_team = models.CharField(max_length=50)
    visiting_team = models.CharField(max_length=50)
    home_coach = models.CharField(max_length=62)
    visiting_coach = models.CharField(max_length=62)

    def __str__(self):
        return f"Home: {self.home_team} -- {self.home_coach}\n" \
               f"Visiting: {self.visiting_team} -- {self.visiting_coach}"


# Scorebook will have a RunningScore with 26 Score entries.
class Score(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.TimeField("Time Scored")
    quarter = models.CharField("Position", max_length=8, choices=QUARTERS, default="")
    goal_number = models.IntegerField("Goal Jersey", null=True)
    assist_number = models.IntegerField("Assist Jersey", null=True)
    running_score = models.ForeignKey(RunningScore, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.goal_number} made a goal at {self.time}."


class Scorebook(models.Model):
    id = models.AutoField(primary_key=True)
    home_coach = models.OneToOneField(Coach, related_name="home_coach", on_delete=models.CASCADE, default=None)
    visiting_coach = models.OneToOneField(Coach, related_name="visiting_coach", on_delete=models.CASCADE, default=None)
    scorekeeper = models.OneToOneField(Scorekeeper, related_name="scorekeeper", on_delete=models.CASCADE, default=None)
    running_score = models.OneToOneField(RunningScore, on_delete=models.CASCADE, default=None)
    time_remaining = None
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Home Team: {self.home_coach}\n" \
               f"Visiting Team: {self.visiting_coach}"


class PlayerStatistics(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, default=None)
    first_quarter = models.BooleanField(default=False)
    second_quarter = models.BooleanField(default=False)
    third_quarter = models.BooleanField(default=False)
    fourth_quarter = models.BooleanField(default=False)
    overtime = models.BooleanField(default=False)
    shots = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    ground_balls = models.IntegerField(null=True)
   # home_statistics = models.ForeignKey(Scorebook, related_name="home_penalties", on_delete=models.CASCADE, default=None)
   # visiting_statistics = models.ForeignKey(Scorebook, related_name="visiting_penalties", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.player}"


class Penalty(models.Model):
    id = models.AutoField(primary_key=True)
    personal_foul = models.BooleanField(default=True)
    player_number = models.IntegerField(null=True)
    infraction = models.CharField(max_length=50)
    quarter = models.CharField(max_length=8, choices=QUARTERS, default="")
    time = models.TimeField()
    home_penalties = models.ForeignKey(Scorebook, related_name="home_penalties", on_delete=models.CASCADE, default=None)
    visiting_penalties = models.ForeignKey(Scorebook, related_name="visiting_penalties", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Player {self.player_number} penalized for {self.time}.\n" \
               f"Reason: {self.infraction}"