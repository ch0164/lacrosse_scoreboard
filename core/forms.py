from django import forms

from core.constants import *
from core.models import Coach, Roster, StartingLineup


class PlayerEntryForm(forms.Form):
    profile_image = forms.ImageField(required=False)
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))
    class_standing = forms.CharField(
        widget=forms.Select(choices=CLASS_STANDING_CHOICES), required=False)
    weight_pounds = forms.IntegerField(min_value=0, required=False)
    height_feet = forms.IntegerField(min_value=0, required=False)
    height_inches = forms.IntegerField(min_value=0, required=False)
    major = forms.CharField(max_length=100, required=False)
    hometown = forms.CharField(max_length=100, required=False)


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
        attackmen = forms.ModelMultipleChoiceField(queryset=attack_set,
                                                   help_text="Select 3 Attackmen")
        midfielders = forms.ModelMultipleChoiceField(queryset=mid_set,
                                                     help_text="Select 3 Midfielders")
        defensemen = forms.ModelMultipleChoiceField(queryset=defend_set,
                                                    help_text="Select 3 Defensemen")
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

    if request.method == "GET":
        form = StartingLineupForm(request.GET)
    else:
        form = StartingLineupForm()

    return form


# Define Scorebook modal forms below.
class CreateScorebookForm(forms.Form):
    home_school = forms.CharField(max_length=100)
    home_team_name = forms.CharField(max_length=50)
    visiting_school = forms.CharField(max_length=100)
    visiting_team_name = forms.CharField(max_length=50)

    # time_created = forms.TimeField()



class ScorebookScoreForm(forms.Form):
    minutes = forms.IntegerField(min_value=0, max_value=90)
    seconds = forms.IntegerField(min_value=0, max_value=59)
    quarter = forms.CharField(widget=forms.HiddenInput(), required=False)
    goal_jersey = forms.IntegerField(min_value=0)
    assist_jersey = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        cleaned_data = super(ScorebookScoreForm, self).clean()

        if "minutes" not in cleaned_data:
            return cleaned_data
        elif cleaned_data["minutes"] < 15:
            cleaned_data["quarter"] = "I"
        elif cleaned_data["minutes"] < 30:
            cleaned_data["quarter"] = "II"
        elif cleaned_data["minutes"] < 45:
            cleaned_data["quarter"] = "III"
        elif cleaned_data["minutes"] < 60:
            cleaned_data["quarter"] = "IV"
        else:
            cleaned_data["quarter"] = "OT"
        return cleaned_data

    # def clean_quarter(self):
    #     self.is_valid()
    #     print(self)
    #     if self.cleaned_data["minutes"] < 15:
    #         return "I"
    #     elif self.cleaned_data["minutes"] < 30:
    #         return "II"
    #     elif self.cleaned_data["minutes"] < 45:
    #         return "II"
    #     elif self.cleaned_data["minutes"] < 60:
    #         return "IV"
    #     else:
    #         return "OT"


def running_score_form_factory(request, scorebook, **kwargs):
    # If the user just lands on the page with a GET request, return an empty form.
    if request.method == "GET":
        return ScorebookScoreForm()

    # Parse the POST request to see if the home/visiting roster should be used.
    if "home" in str(request.POST).lower():
        roster = scorebook.home_coach.roster
    else:
        roster = scorebook.visiting_coach.roster

    # Determine all the valid player numbers for the roster.
    player_numbers = [player.player_number for player in
                      roster.player_set.iterator()]

    # Define a child of the ScoreForm which validates the player numbers.
    class __ScorebookScoreForm(ScorebookScoreForm):
        def clean_goal_jersey(self):
            if self.cleaned_data["goal_jersey"] not in player_numbers:
                print("GOAL JERSEY ERROR")
                self.add_error("goal_jersey", forms.ValidationError(
                    "Goal jersey is not in the selected roster!"))

            if "goal_jersey" in self.cleaned_data:
                return self.cleaned_data["goal_jersey"]
            else:
                return

        def clean_assist_jersey(self):
            if self.cleaned_data["assist_jersey"] is None:
                return
            else:
                if self.cleaned_data["assist_jersey"] not in player_numbers:
                    print(self.cleaned_data["assist_jersey"])
                    print("ASSIST JERSEY ERROR")
                    self.add_error("assist_jersey", forms.ValidationError(
                        "Assist jersey is not in the selected roster!"))

                if "assist_jersey" in self.cleaned_data:
                    return self.cleaned_data["assist_jersey"]
                else:
                    return

    # Return with the new form and pass it the POST request.
    return __ScorebookScoreForm(request.POST, **kwargs)



# Abstract Penalty Form.
class ScorebookPenaltyForm(forms.Form):
    minutes = forms.IntegerField(min_value=0, max_value=90)
    seconds = forms.IntegerField(min_value=0, max_value=59)
    player_number = forms.IntegerField(min_value=0)
    infraction = forms.CharField()
    quarter = forms.CharField(widget=forms.Select(choices=QUARTERS))
    # time = forms.TimeField()


# Personal Foul Penalty Form.
class ScorebookPersonalFoulForm(ScorebookPenaltyForm):
    infraction = forms.CharField(widget=forms.Select(choices=PERSONAL_FOULS))


# Technical Foul Penalty Form
class ScorebookTechnicalFoulForm(ScorebookPenaltyForm):
    infraction = forms.CharField(widget=forms.Select(choices=TECHNICAL_FOULS))


class ScorebookTimeoutForm(forms.Form):
    minutes = forms.IntegerField(min_value=0, max_value=90)
    seconds = forms.IntegerField(min_value=0, max_value=59)
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
