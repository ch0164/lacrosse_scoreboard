from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from core.forms import *
from core.models import *

scorebook_context = {
    "running_score": None,
    "home_penalties": None,
    "visiting_penalties": None,
    "timeouts": None,
    "home_roster": None,
    "visiting_roster": None,
    "running_score_form": ScorebookAddScore(),
    "personal_foul_form": ScorebookPersonalFoul(),
    "technical_foul_form": ScorebookTechnicalFoul(),
    "timeout_form": ScorebookTimeout(),
    "home_penalties_form": ScorebookPenalty(),
    "visiting_penalties_form": ScorebookPenalty(),
    "add_player_form": ScorebookAddPlayer(),
    "import_roster_form": ScorebookImportRoster(),
}

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"scorebooks": Scorebook.objects.all()})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


# Registration view is defined in user_registration/views.py.

def view_scorebook(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebook.html")


@login_required
def edit_scorebook(request: HttpRequest) -> HttpResponse:
    print(scorebook_context)

    # User has submitted a form -- determine which one and handle it.
    if request.method == "POST":
        print(request.POST)

        # User selected the home team's running score.
        if "homeScoreModal" in str(request.POST):
            print("THIS IS A TEST")
            form = ScorebookAddScore(request.POST)
            if form.is_valid():

                if scorebook_context["running_score"] is None:
                    running_score = RunningScore()
                    running_score.save()
                else:
                    running_score = scorebook_context["running_score"]

                score = Score(time=form.cleaned_data.get("time"),
                              quarter=form.cleaned_data.get("quarter"),
                              goal_number=form.cleaned_data.get("goal_jersey"),
                              assist_number=form.cleaned_data.get("assist_jersey"),
                              home_score=running_score)
                score.save()
                scorebook_context["running_score"] = running_score
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected the visiting team's running score.
        elif "visitingScoreModal" in str(request.POST):
            form = ScorebookAddScore(request.POST)
            if form.is_valid():

                if scorebook_context["running_score"] is None:
                    running_score = RunningScore()
                    running_score.save()
                else:
                    running_score = scorebook_context["running_score"]

                score = Score(time=form.cleaned_data.get("time"),
                              quarter=form.cleaned_data.get("quarter"),
                              goal_number=form.cleaned_data.get("goal_jersey"),
                              assist_number=form.cleaned_data.get("assist_jersey"),
                              visiting_score=running_score)
                score.save()
                scorebook_context["running_score"] = running_score
                return HttpResponseRedirect('/edit-scorebook/')

        elif "homePenaltyModal" in str(request.POST):
            pass

        elif "visitingPenaltyModal" in str(request.POST):
            pass

        # User selected to call a timeout for the home team.
        elif "homeTimeoutModal" in str(request.POST):
            form = ScorebookTimeout(request.POST)
            if form.is_valid():
                if scorebook_context["timeouts"] is None:
                    timeouts = TimeoutSet()
                    timeouts.save()
                else:
                    timeouts = scorebook_context["timeouts"]

                timeout = Timeout(time=form.cleaned_data.get("time"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  home_timeouts=timeouts)
                timeout.save()
                scorebook_context["timeouts"] = timeouts
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected to call a timeout for the home team.
        elif "visitingTimeoutModal" in str(request.POST):
            form = ScorebookTimeout(request.POST)
            if form.is_valid():
                if scorebook_context["timeouts"] is None:
                    timeouts = TimeoutSet()
                    timeouts.save()
                else:
                    timeouts = scorebook_context["timeouts"]

                timeout = Timeout(time=form.cleaned_data.get("time"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  visiting_timeouts=timeouts)
                timeout.save()
                scorebook_context["timeouts"] = timeouts
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected a roster for the home team.
        elif "homeImportRosterModal" in str(request.POST):
            roster_id = request.POST.get("roster")[0]
            roster = Roster.objects.filter(id=roster_id)[0]
            scorebook_context["home_roster"] = roster
            return HttpResponseRedirect('/edit-scorebook/')

        # User selected a roster for the home team.
        elif "visitingImportRosterModal" in str(request.POST):
            roster_id = request.POST.get("roster")[0]
            roster = Roster.objects.filter(id=roster_id)[0]
            scorebook_context["visiting_roster"] = roster
            return HttpResponseRedirect('/edit-scorebook/')

    return render(request, "scorebook.html", scorebook_context)


@login_required
def view_roster(request: HttpRequest) -> HttpResponse:
    # NOTE: Temporarily commented out (as well as contents of roster.html).
    # players = Player.objects.all()
    # return render(request, "roster.html", {"players": players})

    # TODO: Add players to the current coach's roster (not a temp one).
    # TODO: Coach needs to create a roster first.
    # Since usernames are unique, find the coach's data from the QuerySet.
    coach = Coach.objects.filter(user=request.user)[0]
    # If the Coach is a new account with no established Roster, have them fill out some info first.
    if coach.roster is None:
        if request.method == "GET":
            form = RosterEntryForm(request.GET)
            # If the form is valid, save the Roster to this Coach and then display it.
            if form.is_valid():
                roster = Roster(team_name=form.cleaned_data.get("team_name"),
                                school=form.cleaned_data.get("school"),
                                win_count=0,
                                loss_count=0)
                roster.save()
                coach.roster = roster
                coach.save()
                return render(request, "roster.html", {"form": PlayerEntryForm(), "has_roster": True, "roster": roster})

        print("test")
        return render(request, "roster.html", {"form": RosterEntryForm(), "has_roster": False})

    # Otherwise, the Coach has established a Roster, so display it.
    else:
        # When the coach enters the player data, handle it here.
        if request.method == "GET":
            form = PlayerEntryForm(request.GET)
            if form.is_valid():
                player = Player(
                    player_number=form.cleaned_data.get("player_number"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    position=form.cleaned_data.get("position"),
                    class_standing=form.cleaned_data.get("class_standing"),
                    weight_pounds=form.cleaned_data.get("weight_pounds"),
                    height_feet=form.cleaned_data.get("height_feet"),
                    height_inches=form.cleaned_data.get("height_inches"),
                    major=form.cleaned_data.get("major"),
                    hometown=form.cleaned_data.get("hometown"),
                    team=coach.roster,
                )
                player.save()
                print(player)

                # Redirect to the root roster page so that the GET request isn't sent again upon refreshing the page.
                return HttpResponseRedirect("/roster/")

        form = PlayerEntryForm()
        players = coach.roster.player_set.all()
        return render(request, "roster.html", {"form": form, "has_roster": True, "players": players, "roster": coach.roster})


@login_required
def edit_player(request: HttpRequest, player_id: int) -> HttpResponse:
    player = Player.objects.get(id=player_id)
    print(player)
    initial = {
        "player_number": player.player_number,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "position": player.position,
        "class_standing": player.class_standing,
        "weight_pounds": player.weight_pounds,
        "height_feet": player.height_feet,
        "height_inches": player.height_inches,
        "major": player.major,
        "hometown": player.hometown
    }

    if player is not None:
        if request.method == "POST":
            form = PlayerEntryForm(request.POST)
            if form.is_valid():
                player.player_number = form.cleaned_data.get("player_number")
                player.first_name = form.cleaned_data.get("first_name")
                player.last_name = form.cleaned_data.get("last_name")
                player.position = form.cleaned_data.get("position")
                player.class_standing = form.cleaned_data.get("class_standing")
                player.weight_pounds = form.cleaned_data.get("weight_pounds")
                player.height_feet = form.cleaned_data.get("height_feet")
                player.height_inches = form.cleaned_data.get("height_inches")
                player.major = form.cleaned_data.get("major")
                player.hometown = form.cleaned_data.get("hometown")
                player.save()
                return HttpResponseRedirect("/roster/")

        form = PlayerEntryForm(initial=initial)
        return render(request, "edit_player.html", {"form": form, "id": player.id})
    else:
        return HttpResponse("Player Not Found")

@login_required
def delete_player(request: HttpRequest, player_id: int) -> HttpResponse:
    player = Player.objects.filter(id=player_id)[0]
    if player is not None:
        player.delete()
        return HttpResponseRedirect("/roster/")
    else:
        return HttpResponse("Player Not Found")
