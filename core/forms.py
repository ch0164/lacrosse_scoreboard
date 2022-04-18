from django import forms

from core.constants import *
from core.models import Coach, Roster


class PlayerEntryForm(forms.Form):
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))
    class_standing = forms.CharField(
        widget=forms.Select(choices=CLASS_STANDING_CHOICES))
    weight_pounds = forms.IntegerField(min_value=0)
    height_feet = forms.IntegerField(min_value=0)
    height_inches = forms.IntegerField(min_value=0)
    major = forms.CharField(max_length=100)
    hometown = forms.CharField(max_length=100)


class RosterEntryForm(forms.Form):
    school = forms.CharField(max_length=100)
    team_name = forms.CharField(max_length=50)


# Define Scorebook modal forms below.
class CreateScorebookForm(forms.Form):
    pass
    # time_created = forms.TimeField()



class ScorebookScoreForm(forms.Form):
    # time = forms.TimeField()
    quarter = forms.CharField(widget=forms.Select(choices=QUARTERS))
    goal_jersey = forms.IntegerField(min_value=0)
    assist_jersey = forms.IntegerField(min_value=0)


# Abstract Penalty Form.
class ScorebookPenaltyForm(forms.Form):
    player_number = forms.IntegerField(min_value=0)
    quarter = forms.CharField(widget=forms.Select(choices=QUARTERS))
    # time = forms.TimeField()
    infraction = forms.CharField()


# Personal Foul Penalty Form.
class ScorebookPersonalFoulForm(ScorebookPenaltyForm):
    infraction = forms.CharField(widget=forms.Select(choices=PERSONAL_FOULS))


# Technical Foul Penalty Form
class ScorebookTechnicalFoulFormForm(ScorebookPenaltyForm):
    infraction = forms.CharField(widget=forms.Select(choices=TECHNICAL_FOULS))


class ScorebookTimeoutForm(forms.Form):
    # time = forms.TimeField()
    quarter = forms.CharField(widget=forms.Select(choices=QUARTERS))

#class ScorebookPenaltyHome(forms.Form):
    #penalties = forms.CharField(widget=forms.Select(choices=Penalties_Home))

#class ScorebookPenaltyVisiting(forms.Form):
    #penalties = forms.CharField(widget=forms.Select(choices=Penalties_Away))


class ScorebookPlayerForm(forms.Form):
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))


class ScorebookImportRoster(forms.Form):
    roster = forms.ModelChoiceField(queryset=Roster.objects.all())
