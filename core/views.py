from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect
from django.shortcuts import render

from core.forms import *
from core.models import *

scorebook_context = {
    "running_score_form": ScorebookScoreForm(),
    "personal_foul_form": ScorebookPersonalFoulForm(),
    "technical_foul_form": ScorebookTechnicalFoulFormForm(),
    "timeout_form": ScorebookTimeoutForm(),
    "home_penalties_form": ScorebookPenaltyForm(),
    "visiting_penalties_form": ScorebookPenaltyForm(),
    "add_player_form": ScorebookPlayerForm(),
    "import_roster_form": ScorebookImportRoster(),
}

scorebook = None


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"scorebooks": Scorebook.objects.all()})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


# Registration view is defined in user_registration/views.py.

def view_scorebook(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebook.html")


@login_required
def create_scorebook(request: HttpRequest) -> HttpResponse:
    global scorebook
    form = CreateScorebookForm()
    if request.method == "POST":
        form = CreateScorebookForm(request.POST)
        if form.is_valid():
            # Create rosters.
            home_roster = Roster()
            home_roster.save()
            visiting_roster = Roster()
            visiting_roster.save()

            # Create coaches.
            home_coach = Coach(roster=home_roster)
            home_coach.save()
            visiting_coach = Coach(roster=visiting_roster)
            visiting_coach.save()

            # Create running score models.
            running_score = RunningScore()
            running_score.save()

            # Create timeout set models.
            timeouts = TimeoutSet()
            timeouts.save()

            # Create penalty set models.
            penalties = PenaltySet()
            penalties.save()

            # Create scorebook.
            scorebook = Scorebook(home_coach=home_coach,
                                  visiting_coach=visiting_coach,
                                  running_score=running_score,
                                  timeouts=timeouts,
                                  penalties=penalties)
            scorebook.save()

            # Save scorebook to context.
            scorebook_context["scorebook"] = scorebook
            return HttpResponseRedirect('/edit-scorebook/')
    return render(request, "create_scorebook.html", {"form": form})


@login_required
def edit_scorebook(request: HttpRequest) -> HttpResponse:
    global scorebook
    if scorebook is None:
        return HttpResponseRedirect('/create-scorebook/')

    # User has submitted a form -- determine which one and handle it.
    if request.method == "POST":
        # User selected the home team's running score.
        if "homeScoreModal" in str(request.POST):
            form = ScorebookScoreForm(request.POST)
            if form.is_valid():
                score = Score(time=form.cleaned_data.get("time"),
                              quarter=form.cleaned_data.get("quarter"),
                              goal_number=form.cleaned_data.get("goal_jersey"),
                              assist_number=form.cleaned_data.get(
                                  "assist_jersey"),
                              home_score=scorebook.running_score)
                score.save()
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected the visiting team's running score.
        elif "visitingScoreModal" in str(request.POST):
            form = ScorebookScoreForm(request.POST)
            if form.is_valid():
                score = Score(time=form.cleaned_data.get("time"),
                              quarter=form.cleaned_data.get("quarter"),
                              goal_number=form.cleaned_data.get("goal_jersey"),
                              assist_number=form.cleaned_data.get(
                                  "assist_jersey"),
                              visiting_score=scorebook.running_score)
                score.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "homePersonalFoulModal" in str(request.POST):
            form = ScorebookPersonalFoulForm(request.POST)
            if form.is_valid():
                penalty = Penalty(personal_foul=True,
                                  player_number=form.cleaned_data.get(
                                      "player_number"),
                                  infraction=form.cleaned_data.get(
                                      "infraction"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  time=form.cleaned_data.get("time"),
                                  home_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "homeTechnicalFoulModal" in str(request.POST):
            form = ScorebookPersonalFoulForm(request.POST)
            if form.is_valid():
                penalty = Penalty(personal_foul=False,
                                  player_number=form.cleaned_data.get(
                                      "player_number"),
                                  infraction=form.cleaned_data.get(
                                      "infraction"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  time=form.cleaned_data.get("time"),
                                  home_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "visitingPersonalFoulModal" in str(request.POST):
            form = ScorebookPersonalFoulForm(request.POST)
            if form.is_valid():
                penalty = Penalty(personal_foul=True,
                                  player_number=form.cleaned_data.get(
                                      "player_number"),
                                  infraction=form.cleaned_data.get(
                                      "infraction"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  time=form.cleaned_data.get("time"),
                                  visiting_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "visitingTechnicalFoulModal" in str(request.POST):
            form = ScorebookPersonalFoulForm(request.POST)
            if form.is_valid():
                penalty = Penalty(personal_foul=False,
                                  player_number=form.cleaned_data.get(
                                      "player_number"),
                                  infraction=form.cleaned_data.get(
                                      "infraction"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  time=form.cleaned_data.get("time"),
                                  visiting_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected to call a timeout for the home team.
        elif "homeTimeoutModal" in str(request.POST):
            form = ScorebookTimeoutForm(request.POST)
            if form.is_valid():
                timeout = Timeout(time=form.cleaned_data.get("time"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  home_timeouts=scorebook.timeouts)
                timeout.save()
                return HttpResponseRedirect('/edit-scorebook/')

        # User selected to call a timeout for the home team.
        elif "visitingTimeoutModal" in str(request.POST):
            form = ScorebookTimeoutForm(request.POST)
            if form.is_valid():
                timeout = Timeout(time=form.cleaned_data.get("time"),
                                  quarter=form.cleaned_data.get("quarter"),
                                  visiting_timeouts=scorebook.timeouts)
                timeout.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "homeAddPlayerModal" in str(request.POST):
            form = ScorebookPlayerForm(request.POST)
            if form.is_valid():
                player = Player(
                    player_number=form.cleaned_data.get("player_number"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    position=form.cleaned_data.get("position"),
                    team=scorebook.home_coach.roster)
                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

        # User selected a roster for the home team.
        elif "homeImportRosterModal" in str(request.POST):
            roster_id = request.POST.get("roster")
            roster = Roster.objects.filter(id=roster_id)[0]
            scorebook.home_coach.roster = roster
            scorebook.save()
            return HttpResponseRedirect('/edit-scorebook/')

        elif "visitingAddPlayerModal" in str(request.POST):
            form = ScorebookPlayerForm(request.POST)
            if form.is_valid():
                player = Player(
                    player_number=form.cleaned_data.get("player_number"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    position=form.cleaned_data.get("position"),
                    team=scorebook.visiting_coach.roster)
                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

        # User selected a roster for the home team.
        elif "visitingImportRosterModal" in str(request.POST):
            roster_id = request.POST.get("roster")
            roster = Roster.objects.filter(id=roster_id)[0]
            scorebook.visiting_coach.roster = roster
            scorebook.save()
            return HttpResponseRedirect('/edit-scorebook/')

        # User selected to clear the roster.
        elif "clearScorebookModal" in str(request.POST):
            if scorebook is not None:
                scorebook.delete()
                scorebook = None
                scorebook_context.pop("scorebook")
                return HttpResponseRedirect('/create-scorebook/')

    # Handle all data modification if a GET request is sent via Ajax.
    elif request.method == "GET":
        # What is the model's ID?
        id = request.GET.get('id', '')
        # Does the user want to 'edit' or 'delete' the model?
        type = request.GET.get('type', '')
        # Which model does the user want to modify?
        model = request.GET.get('model', '')

        print(id, type, model)

    scorebook_context["scorebook"] = scorebook
    return render(request, "scorebook.html", scorebook_context)


@login_required
def scorebook_edit_score(request: HttpRequest, score_id: int) -> HttpResponse:
    score = Score.objects.get(id=score_id)
    initial = {
        "quarter": score.quarter,
        "goal_jersey": score.goal_number,
        "assist_jersey": score.assist_number,
    }

    if score is not None:
        if request.method == "POST":
            form = ScorebookScoreForm(request.POST)
            if form.is_valid():
                score.quarter = form.cleaned_data.get("quarter")
                score.goal_number = form.cleaned_data.get("goal_jersey")
                score.assist_number = form.cleaned_data.get("assist_jersey")
                score.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = ScorebookScoreForm(initial=initial)
        return render(request, "edit_score.html",
                      {"form": form, "id": score.id})
    else:
        return HttpResponse("Running Score Not Found")


@login_required
def scorebook_edit_personal_foul(request: HttpRequest,
                                 penalty_id: int) -> HttpResponse:
    penalty = Penalty.objects.get(id=penalty_id)
    initial = {
        "player_number": penalty.player_number,
        "infraction": penalty.infraction,
        "quarter": penalty.quarter,
    }

    if penalty is not None:
        if request.method == "POST":
            form = ScorebookPersonalFoulForm(request.POST)
            if form.is_valid():
                penalty.player_number = form.cleaned_data.get("player_number")
                penalty.infraction = form.cleaned_data.get("infraction")
                penalty.quarter = form.cleaned_data.get("quarter")
                penalty.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = ScorebookPersonalFoulForm(initial=initial)
        return render(request, "edit_personal_foul.html",
                      {"form": form, "id": penalty.id})
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_edit_technical_foul(request: HttpRequest,
                                  penalty_id: int) -> HttpResponse:
    penalty = Penalty.objects.get(id=penalty_id)
    initial = {
        "player_number": penalty.player_number,
        "infraction": penalty.infraction,
        "quarter": penalty.quarter,
    }

    if penalty is not None:
        if request.method == "POST":
            form = ScorebookTechnicalFoulFormForm(request.POST)
            if form.is_valid():
                penalty.player_number = form.cleaned_data.get("player_number")
                penalty.infraction = form.cleaned_data.get("infraction")
                penalty.quarter = form.cleaned_data.get("quarter")
                penalty.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = ScorebookTechnicalFoulFormForm(initial=initial)
        return render(request, "edit_technical_foul.html",
                      {"form": form, "id": penalty.id})
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_edit_timeout(request: HttpRequest,
                           timeout_id: int) -> HttpResponse:
    timeout = Timeout.objects.get(id=timeout_id)
    initial = {
        "quarter": timeout.quarter,
    }

    if timeout is not None:
        if request.method == "POST":
            form = ScorebookTimeoutForm(request.POST)
            if form.is_valid():
                timeout.quarter = form.cleaned_data.get("quarter")
                timeout.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = ScorebookTimeoutForm(initial=initial)
        return render(request, "edit_timeout.html",
                      {"form": form, "id": timeout.id})
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_edit_player(request: HttpRequest, player_id: int) -> HttpResponse:
    player = Player.objects.get(id=player_id)
    initial = {
        "player_number": player.player_number,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "position": player.position,
    }

    if player is not None:
        if request.method == "POST":
            form = ScorebookPlayerForm(request.POST)
            if form.is_valid():
                player.player_number = form.cleaned_data.get("player_number")
                player.first_name = form.cleaned_data.get("first_name")
                player.last_name = form.cleaned_data.get("last_name")
                player.position = form.cleaned_data.get("position")
                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = ScorebookPlayerForm(initial=initial)
        return render(request, "edit_scorebook_player.html",
                      {"form": form, "id": player.id})
    else:
        return HttpResponse("Player Not Found")


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
                return render(request, "roster.html",
                              {"form": PlayerEntryForm(), "has_roster": True,
                               "roster": roster})

        print("test")
        return render(request, "roster.html",
                      {"form": RosterEntryForm(), "has_roster": False})

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
        return render(request, "roster.html",
                      {"form": form, "has_roster": True, "players": players,
                       "roster": coach.roster})


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
        return render(request, "edit_player.html",
                      {"form": form, "id": player.id})
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
