from django import forms

from core.constants import *
from core.models import Coach, Roster, StartingLineup


class PlayerEntryForm(forms.Form):
    profile_image = forms.ImageField(required=False, )
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))
    class_standing = forms.CharField(
        widget=forms.Select(choices=CLASS_STANDING_CHOICES))
    weight_pounds = forms.IntegerField(min_value=0)
    height_feet = forms.IntegerField(min_value=0)
    height_inches = forms.IntegerField(min_value=0)
    major = forms.CharField(max_length=100, required=False)
    hometown = forms.CharField(max_length=100)


class RosterEntryForm(forms.Form):
    school = forms.CharField(max_length=100)
    team_name = forms.CharField(max_length=50)


# Create a form that restricts available players to those within
# the coach's roster.
def starting_lineup_form_factory(request):
    # Get this coach user's roster.
    coach = Coach.objects.filter(user=request.user)[0]
    roster = coach.roster
    player_set = roster.player_set.all()

    # Partition the roster into four core positions.
    attack_ids, mid_ids, defend_ids, goalie_ids = [], [], [], []
    for player in player_set:
        if player.position in "ATT":
            attack_ids.append(player.id)
        elif player.position in ["MID", "SSDM", "LSM", "FOGO"]:
            mid_ids.append(player.id)
        elif player.position in "DEF":
            defend_ids.append(player.id)
        else:
            goalie_ids.append(player.id)

    # Convert to querysets.
    attack_set = player_set.filter(id__in=attack_ids)
    mid_set = player_set.filter(id__in=mid_ids)
    defend_set = player_set.filter(id__in=defend_ids)
    goalie_set = player_set.filter(id__in=goalie_ids)

    # Create the form using the created querysets.
    # A lacrosse team can only have ten players on the field.
    class StartingLineupForm(forms.Form):
        attackmen = forms.ModelMultipleChoiceField(queryset=attack_set, help_text="Select 3 Attackmen")
        midfielders = forms.ModelMultipleChoiceField(queryset=mid_set, help_text="Select 3 Midfielders")
        defensemen = forms.ModelMultipleChoiceField(queryset=defend_set, help_text="Select 3 Defensemen")
        goalie = forms.ModelChoiceField(widget=forms.Select,
                                        queryset=goalie_set)

        def clean_attackmen(self):
            attackmen = self.cleaned_data["attackmen"]
            if len(attackmen) < 3 or len(attackmen) > 3:
                self.add_error("attackmen", forms.ValidationError(
                    "You must select exactly three attackmen."))
            return attackmen

        def clean_midfielders(self):
            midfielders = self.cleaned_data["midfielders"]
            if len(midfielders) < 3 or len(midfielders) > 3:
                self.add_error("midfielders", forms.ValidationError(
                    "You must select exactly three midfielders."))
            return midfielders

        def clean_defensemen(self):
            defensemen = self.cleaned_data["defensemen"]
            if len(defensemen) < 3 or len(defensemen) > 3:
                self.add_error("defensemen", forms.ValidationError(
                    "You must select exactly three defensemen."))
            return defensemen

    if request.method == "POST":
        form = StartingLineupForm(request.POST)
    else:
        form = StartingLineupForm()

    return form


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
class ScorebookTechnicalFoulForm(ScorebookPenaltyForm):
    infraction = forms.CharField(widget=forms.Select(choices=TECHNICAL_FOULS))


class ScorebookTimeoutForm(forms.Form):
    # time = forms.TimeField()
    quarter = forms.CharField(widget=forms.Select(choices=QUARTERS))


# class ScorebookPenaltyHome(forms.Form):
# penalties = forms.CharField(widget=forms.Select(choices=Penalties_Home))

# class ScorebookPenaltyVisiting(forms.Form):
# penalties = forms.CharField(widget=forms.Select(choices=Penalties_Away))


class ScorebookPlayerForm(forms.Form):
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))


class ScorebookImportLineup(forms.Form):
    lineup = forms.ModelChoiceField(queryset=StartingLineup.objects.all())
