import datetime

from django.contrib.auth.models import User
from django.db import models

from core.constants import *
from scoreboard.settings import AUTH_USER_MODEL


class Roster(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, default="")
    school = models.CharField(max_length=100, default="")
    win_count = models.PositiveIntegerField(default=0)
    loss_count = models.PositiveIntegerField(default=0)
    # TODO: Change below default to False and add publish button.
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.school} {self.team_name}"  # Example: "UAH Chargers"


class PlayerStatistics(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    first_quarter = models.BooleanField(default=False)
    second_quarter = models.BooleanField(default=False)
    third_quarter = models.BooleanField(default=False)
    fourth_quarter = models.BooleanField(default=False)
    overtime = models.BooleanField(default=False)
    shots = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    ground_balls = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"I: {self.first_quarter}, II: {self.second_quarter}, " \
               f"III: {self.third_quarter}, IV: {self.fourth_quarter}, " \
               f"OT: {self.overtime}\n" \
               f"S: {self.shots}, G: {self.goals}, A: {self.assists}, GB: {self.ground_balls}"


class PlayerSaves(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    first_quarter = models.PositiveIntegerField(default=0)
    second_quarter = models.PositiveIntegerField(default=0)
    third_quarter = models.PositiveIntegerField(default=0)
    fourth_quarter = models.PositiveIntegerField(default=0)
    overtime = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"I: {self.first_quarter}, II: {self.second_quarter}, " \
               f"III: {self.third_quarter}, IV: {self.fourth_quarter}, " \
               f"OT: {self.overtime}"


class Player(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    profile_image = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/default.jpg")
    player_number = models.PositiveIntegerField("Player Number", default=0)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    position = models.CharField("Position", max_length=4,
                                choices=POSITION_CHOICES, default="ATT")
    class_standing = models.CharField("Class", max_length=2,
                                      choices=CLASS_STANDING_CHOICES,
                                      default="N/A")
    weight_pounds = models.PositiveIntegerField("Weight (pounds)", default=0, blank=True, null=True)
    height_feet = models.PositiveIntegerField("Height (feet)", default=0, blank=True, null=True)
    height_inches = models.PositiveIntegerField("Height (inches)", default=0, blank=True, null=True)
    major = models.CharField("Major", max_length=100, default="N/A", blank=True, null=True)
    hometown = models.CharField("Hometown", max_length=100, default="N/A", blank=True, null=True)
    # Relationships
    team = models.ForeignKey(Roster,
                             on_delete=models.CASCADE,
                             default=None)
    statistics = models.ForeignKey(PlayerStatistics,
                                   related_name="statistics",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    saves = models.ForeignKey(PlayerSaves,
                              related_name="saves",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              default=None)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (#{self.player_number})"


class StartingLineup(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    school = models.CharField(max_length=100, default="")
    team_name = models.CharField(max_length=50, default="")
    coach_first_name = models.CharField(max_length=50, default="")
    coach_last_name = models.CharField(max_length=50, default="")
    # Relationships
    attacker_1 = models.ForeignKey(Player,
                                   related_name="attacker_1",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    attacker_2 = models.ForeignKey(Player,
                                   related_name="attacker_2",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    attacker_3 = models.ForeignKey(Player,
                                   related_name="attacker_3",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    midfielder_1 = models.ForeignKey(Player,
                                     related_name="midfielder_1",
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     default=None)
    midfielder_2 = models.ForeignKey(Player,
                                     related_name="midfielder_2",
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     default=None)
    midfielder_3 = models.ForeignKey(Player,
                                     related_name="midfielder_3",
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     default=None)
    defender_1 = models.ForeignKey(Player,
                                   related_name="defender_1",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    defender_2 = models.ForeignKey(Player,
                                   related_name="defender_2",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    defender_3 = models.ForeignKey(Player,
                                   related_name="defender_3",
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   default=None)
    goalie = models.ForeignKey(Player,
                               related_name="goalie",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               default=None)

    def __str__(self):
        return f"Head Coach: {self.coach_last_name}, {self.coach_first_name}\n" \
               f"Team: {self.school} {self.team_name}"


class Coach(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    # Relationships
    user = models.OneToOneField(AUTH_USER_MODEL,
                                related_name="coach_user",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                default=None)
    roster = models.OneToOneField(Roster,
                                  related_name="roster",
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE,
                                  default=None)
    starting_lineup = models.OneToOneField(StartingLineup,
                                           related_name="starting_lineup",
                                           null=True,
                                           blank=True,
                                           on_delete=models.CASCADE,
                                           default=None)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Scorekeeper(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=30, default="")
    last_name = models.CharField("Last Name", max_length=30, default="")
    # Relationships
    user = models.OneToOneField(AUTH_USER_MODEL,
                                related_name="scorekeeper_user",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                default=None)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class RunningScore(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)


class Score(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    time = models.TimeField(auto_now=True)
    quarter = models.CharField(max_length=8, choices=QUARTERS, default="")
    goal_number = models.PositiveIntegerField("Goal Jersey", default=0)
    assist_number = models.PositiveIntegerField("Assist Jersey", blank=True,
                                                null=True)
    # Relationships
    home_score = models.ForeignKey(RunningScore,
                                   related_name="home",
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   default=None)
    visiting_score = models.ForeignKey(RunningScore,
                                       related_name="visiting",
                                       null=True,
                                       blank=True,
                                       on_delete=models.CASCADE,
                                       default=None)

    def __str__(self):
        return f"{self.goal_number} made a goal at {self.time}"


class PenaltySet(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)


class Penalty(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    personal_foul = models.BooleanField(default=False)
    player_number = models.PositiveIntegerField(default=0)
    infraction = models.CharField(max_length=50, default="")
    quarter = models.CharField(max_length=8, choices=QUARTERS, default="")
    time = models.TimeField(auto_now=True)
    # Relationships
    home_penalties = models.ForeignKey(PenaltySet,
                                       related_name="home",
                                       null=True,
                                       blank=True,
                                       on_delete=models.CASCADE,
                                       default=None)
    visiting_penalties = models.ForeignKey(PenaltySet,
                                           related_name="visiting",
                                           null=True,
                                           blank=True,
                                           on_delete=models.CASCADE,
                                           default=None)

    def __str__(self):
        return f"Player {self.player_number} penalized for {self.time.strftime('%M:%S')}.\n" \
               f"Reason: {self.infraction}"


class TimeoutSet(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)


class Timeout(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    time = models.TimeField(auto_now=True)
    quarter = models.CharField(max_length=8, choices=QUARTERS, default="")
    # Relationships
    home_timeouts = models.ForeignKey(TimeoutSet,
                                      related_name="home",
                                      null=True,
                                      blank=True,
                                      on_delete=models.CASCADE,
                                      default=None)
    visiting_timeouts = models.ForeignKey(TimeoutSet,
                                          related_name="visiting",
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE,
                                          default=None)


class Scorebook(models.Model):
    # Attributes
    id = models.AutoField(primary_key=True)
    home_score = models.PositiveIntegerField(default=0)
    visiting_score = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    time_remaining = models.TimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now=True)
    # Relationships
    home_coach = models.OneToOneField(Coach,
                                      related_name="home_coach",
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True,
                                      default=None)
    visiting_coach = models.OneToOneField(Coach,
                                          related_name="visiting_coach",
                                          on_delete=models.CASCADE,
                                          null=True,
                                          blank=True,
                                          default=None)
    # scorekeeper = models.OneToOneField(Scorekeeper,
    #                                    on_delete=models.CASCADE,
    #                                    null=True,
    #                                    blank=True,
    #                                    default=None)
    running_score = models.OneToOneField(RunningScore,
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         default=None)
    timeouts = models.OneToOneField(TimeoutSet,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    default=None)
    penalties = models.OneToOneField(PenaltySet,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     default=None)

    def __str__(self):
        # return f"Home Team: {self.home_coach.roster} -- Head Coach: {self.home_coach} -- Score: {self.home_score}\n" \
        #        f"Visiting Team: {self.visiting_coach.roster} -- Head Coach: {self.visiting_coach} -- Score: {self.visiting_score}"
        return f"Scorebook Id: {self.id}"
