import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt



from core.forms import *
from core.models import *
from core.utilities import copy_player

scorebook_context = {
    "scorebook": None,
    "import_lineup_form": ScorebookImportLineup(),
    "run_time_mode": False
}

roster_context = {"has_roster": True, "player_entry_form": PlayerEntryForm()}

initial_time = {"minutes": None, "seconds": None}

total_seconds = 0

scorebook = None

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html",
                  {"scorebooks": Scorebook.objects.filter(is_published=True)})

def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


# Registration view is defined in user_registration/views.py.

def view_scorebook(request: HttpRequest, scorebook_id: int) -> HttpResponse:
    scorebook = Scorebook.objects.filter(id=scorebook_id).first()
    if scorebook is not None:
        return render(request, "view_scorebook.html", {"scorebook": scorebook})
    else:
        return HttpResponse("Scorebook does not exist!")


@login_required
def create_scorebook(request: HttpRequest) -> HttpResponse:
    global scorebook
    form = CreateScorebookForm()
    if request.method == "POST":
        form = CreateScorebookForm(request.POST)
        if form.is_valid():
            # Create rosters.
            home_roster = Roster(school=form.cleaned_data["home_school"],
                                 team_name=form.cleaned_data["home_team_name"])
            home_roster.save()
            visiting_roster = Roster(
                school=form.cleaned_data["visiting_school"],
                team_name=form.cleaned_data["visiting_team_name"])
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
                                  penalties=penalties,
                                  time_elapsed=datetime.timedelta(minutes=0,
                                                                  seconds=0))
            scorebook.save()

            # Save scorebook to context.
            scorebook_context["scorebook"] = scorebook
            return HttpResponseRedirect('/edit-scorebook/')
    return render(request, "create_scorebook.html", {"form": form})


@login_required
# @csrf_exempt
def edit_scorebook(request: HttpRequest) -> HttpResponse:
    global scorebook, initial_time, scorebook_context, total_seconds
    if scorebook is None:
        return HttpResponseRedirect('/create-scorebook/')

    # User has submitted a form -- determine which one and handle it.
    if request.method == "POST":
        # User hit the run time mode button.
        if "runTimeMode" in str(request.POST):
            scorebook_context["run_time_mode"] = not scorebook_context["run_time_mode"]
            if scorebook_context["run_time_mode"]:
                # TODO: Rid of this design
                initial_time = {
                    # "minutes": int(total_seconds // 60),
                    # "seconds": int(total_seconds % 60)
                }
            else:
                initial_time = {
                    # "minutes": None,
                    # "seconds": None
                }

            return render(request, "scorebook.html", scorebook_context)

        # User selected the home team's running score.
        if "homeScoreModal" in str(request.POST):
            home_running_score_form = running_score_form_factory(request,
                                                                 scorebook,
                                                                 initial=initial_time)
            if home_running_score_form.is_valid():
                time = datetime.timedelta(
                    minutes=home_running_score_form.cleaned_data["minutes"],
                    seconds=home_running_score_form.cleaned_data["seconds"])
                score = Score(time=time,
                              quarter=home_running_score_form.cleaned_data.get(
                                  "quarter"),
                              goal_number=home_running_score_form.cleaned_data.get(
                                  "goal_jersey"),
                              assist_number=home_running_score_form.cleaned_data.get(
                                  "assist_jersey"),
                              home_score=scorebook.running_score)
                score.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "home_running_score_form"] = home_running_score_form
        else:
            scorebook_context["home_running_score_form"] = ScorebookScoreForm(initial=initial_time)

        # User selected the visiting team's running score.
        if "visitingScoreModal" in str(request.POST):
            visiting_running_score_form = running_score_form_factory(request,
                                                                     scorebook,
                                                                     initial=initial_time)
            if visiting_running_score_form.is_valid():
                time = datetime.timedelta(
                    minutes=visiting_running_score_form.cleaned_data["minutes"],
                    seconds=visiting_running_score_form.cleaned_data["seconds"])
                score = Score(time=time,
                              quarter=visiting_running_score_form.cleaned_data.get(
                                  "quarter"),
                              goal_number=visiting_running_score_form.cleaned_data.get(
                                  "goal_jersey"),
                              assist_number=visiting_running_score_form.cleaned_data.get(
                                  "assist_jersey"),
                              visiting_score=scorebook.running_score)
                score.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "visiting_running_score_form"] = visiting_running_score_form
        else:
            scorebook_context[
                "visiting_running_score_form"] = ScorebookScoreForm(initial=initial_time)

        # User selected the home team's personal fouls.
        if "homePersonalFoulModal" in str(request.POST):
            home_personal_foul_form = penalty_form_factory(request, scorebook,
                                                           True, initial=initial_time)
            if home_personal_foul_form.is_valid():
                time = datetime.timedelta(
                    minutes=home_personal_foul_form.cleaned_data["minutes"],
                    seconds=home_personal_foul_form.cleaned_data["seconds"])
                penalty = Penalty(personal_foul=True,
                                  player_number=home_personal_foul_form.cleaned_data.get(
                                      "player_number"),
                                  infraction=home_personal_foul_form.cleaned_data.get(
                                      "infraction"),
                                  quarter=home_personal_foul_form.cleaned_data.get(
                                      "quarter"),
                                  time=time,
                                  home_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "home_personal_foul_form"] = home_personal_foul_form
        else:
            scorebook_context[
                "home_personal_foul_form"] = ScorebookPersonalFoulForm(initial=initial_time)

        # User selected the home team's technical fouls.
        if "homeTechnicalFoulModal" in str(request.POST):
            home_technical_foul_form = penalty_form_factory(request, scorebook,
                                                            False, initial=initial_time)
            if home_technical_foul_form.is_valid():
                time = datetime.timedelta(
                    minutes=home_technical_foul_form.cleaned_data["minutes"],
                    seconds=home_technical_foul_form.cleaned_data["seconds"])
                penalty = Penalty(personal_foul=False,
                                  player_number=home_technical_foul_form.cleaned_data.get(
                                      "player_number"),
                                  infraction=home_technical_foul_form.cleaned_data.get(
                                      "infraction"),
                                  quarter=home_technical_foul_form.cleaned_data.get(
                                      "quarter"),
                                  time=time,
                                  home_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "home_technical_foul_form"] = home_technical_foul_form
        else:
            scorebook_context[
                "home_technical_foul_form"] = ScorebookTechnicalFoulForm(initial=initial_time)

        # User selected the visiting team's personal fouls.
        if "visitingPersonalFoulModal" in str(request.POST):
            visiting_personal_foul_form = penalty_form_factory(request,
                                                               scorebook, True, initial=initial_time)
            if visiting_personal_foul_form.is_valid():
                time = datetime.timedelta(
                    minutes=visiting_personal_foul_form.cleaned_data["minutes"],
                    seconds=visiting_personal_foul_form.cleaned_data["seconds"])
                penalty = Penalty(personal_foul=True,
                                  player_number=visiting_personal_foul_form.cleaned_data.get(
                                      "player_number"),
                                  infraction=visiting_personal_foul_form.cleaned_data.get(
                                      "infraction"),
                                  quarter=visiting_personal_foul_form.cleaned_data.get(
                                      "quarter"),
                                  time=time,
                                  visiting_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "visiting_personal_foul_form"] = visiting_personal_foul_form
        else:
            scorebook_context[
                "visiting_personal_foul_form"] = ScorebookPersonalFoulForm(initial=initial_time)

        # User selected the visiting team's technical fouls.
        if "visitingTechnicalFoulModal" in str(request.POST):
            visiting_technical_foul_form = penalty_form_factory(request,
                                                                scorebook,
                                                                False, initial=initial_time)
            if visiting_technical_foul_form.is_valid():
                time = datetime.timedelta(
                    minutes=visiting_technical_foul_form.cleaned_data[
                        "minutes"],
                    seconds=visiting_technical_foul_form.cleaned_data[
                        "seconds"])
                penalty = Penalty(personal_foul=False,
                                  player_number=visiting_technical_foul_form.cleaned_data.get(
                                      "player_number"),
                                  infraction=visiting_technical_foul_form.cleaned_data.get(
                                      "infraction"),
                                  quarter=visiting_technical_foul_form.cleaned_data.get(
                                      "quarter"),
                                  time=time,
                                  visiting_penalties=scorebook.penalties)
                penalty.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "visiting_technical_foul_form"] = visiting_technical_foul_form
        else:
            scorebook_context[
                "visiting_technical_foul_form"] = ScorebookTechnicalFoulForm(initial=initial_time)

        # User selected to call a timeout for the home team.
        if "homeTimeoutModal" in str(request.POST):
            home_timeout_form = timeout_form_factory(request,
                                                     scorebook=scorebook, initial=initial_time)
            if home_timeout_form.is_valid():
                time = datetime.timedelta(
                    minutes=home_timeout_form.cleaned_data["minutes"],
                    seconds=home_timeout_form.cleaned_data["seconds"])
                timeout = Timeout(time=time,
                                  quarter=home_timeout_form.cleaned_data.get(
                                      "quarter"),
                                  home_timeouts=scorebook.timeouts)
                timeout.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "home_timeout_form"] = home_timeout_form
        else:
            scorebook_context[
                "home_timeout_form"] = ScorebookTimeoutForm(initial=initial_time)

        # User selected to call a timeout for the home team.
        if "visitingTimeoutModal" in str(request.POST):
            visiting_timeout_form = timeout_form_factory(request,
                                                         scorebook=scorebook, initial=initial_time)
            if visiting_timeout_form.is_valid():
                time = datetime.timedelta(
                    minutes=visiting_timeout_form.cleaned_data["minutes"],
                    seconds=visiting_timeout_form.cleaned_data["seconds"])
                timeout = Timeout(time=time,
                                  quarter=visiting_timeout_form.cleaned_data.get(
                                      "quarter"),
                                  visiting_timeouts=scorebook.timeouts)
                timeout.save()
                return HttpResponseRedirect('/edit-scorebook/')

            scorebook_context[
                "visiting_timeout_form"] = visiting_timeout_form
        else:
            scorebook_context[
                "visiting_timeout_form"] = ScorebookTimeoutForm(initial=initial_time)

        if "homeAddPlayerModal" in str(request.POST):
            home_add_player_form = player_form_factory(request, scorebook, initial=initial_time)
            if home_add_player_form.is_valid():
                statistics = PlayerStatistics()
                statistics.save()
                saves = PlayerSaves()
                saves.save()

                player = Player(
                    player_number=home_add_player_form.cleaned_data.get(
                        "player_number"),
                    first_name=home_add_player_form.cleaned_data.get(
                        "first_name"),
                    last_name=home_add_player_form.cleaned_data.get(
                        "last_name"),
                    position=home_add_player_form.cleaned_data.get("position"),
                    team=scorebook.home_coach.roster,
                    statistics=statistics,
                    saves=saves)

                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

            scorebook_context[
                "home_add_player_form"] = home_add_player_form
        else:
            scorebook_context[
                "home_add_player_form"] = ScorebookPlayerForm()

        # User selected a roster for the home team.
        if "homeImportLineupModal" in str(request.POST):
            home_import_lineup_form = ScorebookImportLineup(request.POST)
            if home_import_lineup_form.is_valid():
                lineup = home_import_lineup_form.cleaned_data["lineup"]
                # Add players from the lineup to the roster.
                # Check if empty.
                if not scorebook.home_coach.roster:
                    print("NEW ROSTER")
                    roster = Roster()
                    roster.save()

                # Otherwise, just use the Roster that the coach has.
                else:
                    print(scorebook.home_coach.roster)
                    print("REUSED ROSTER")
                    roster = scorebook.home_coach.roster

                players = [
                              lineup.attacker_1,
                              lineup.attacker_2,
                              lineup.attacker_3,
                              lineup.midfielder_1,
                              lineup.midfielder_2,
                              lineup.midfielder_3,
                              lineup.defender_1,
                              lineup.defender_2,
                              lineup.defender_3,
                              lineup.goalie,
                          ] + list(lineup.substitutes.substitute_set.all())
                for player in players:
                    player_copy = copy_player(player)
                    player_copy.team = roster
                    if not player.substitute:
                        player_copy.statistics.first_quarter = True
                        player_copy.statistics.save()
                    player_copy.save()

                # Overwrite the current roster with this new roster.
                scorebook.home_coach.roster = roster
                scorebook.home_coach.save()
                return HttpResponseRedirect('/edit-scorebook/')

        if "visitingAddPlayerModal" in str(request.POST):
            visiting_add_player_form = player_form_factory(request, scorebook, initial=initial_time)
            if visiting_add_player_form.is_valid():
                statistics = PlayerStatistics()
                statistics.save()
                saves = PlayerSaves()
                saves.save()

                player = Player(
                    player_number=visiting_add_player_form.cleaned_data.get(
                        "player_number"),
                    first_name=visiting_add_player_form.cleaned_data.get(
                        "first_name"),
                    last_name=visiting_add_player_form.cleaned_data.get(
                        "last_name"),
                    position=visiting_add_player_form.cleaned_data.get(
                        "position"),
                    team=scorebook.visiting_coach.roster,
                    statistics=statistics,
                    saves=saves)

                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

            scorebook_context[
                "visiting_add_player_form"] = visiting_add_player_form
        else:
            scorebook_context[
                "visiting_add_player_form"] = ScorebookPlayerForm()

        # User selected a lineup for the visiting team.
        if "visitingImportLineupModal" in str(request.POST):
            visiting_import_lineup_form = ScorebookImportLineup(request.POST)
            if visiting_import_lineup_form.is_valid():
                lineup = visiting_import_lineup_form.cleaned_data["lineup"]
                # Add players from the lineup to the roster.
                # Check if empty.
                if not scorebook.visiting_coach.roster:
                    roster = Roster()
                    roster.save()
                else:
                    roster = scorebook.visiting_coach.roster

                players = [
                              lineup.attacker_1,
                              lineup.attacker_2,
                              lineup.attacker_3,
                              lineup.midfielder_1,
                              lineup.midfielder_2,
                              lineup.midfielder_3,
                              lineup.defender_1,
                              lineup.defender_2,
                              lineup.defender_3,
                              lineup.goalie,
                          ] + list(lineup.substitutes.substitute_set.all())
                for player in players:
                    player_copy = copy_player(player)
                    player_copy.team = roster
                    if not player.substitute:
                        player_copy.statistics.first_quarter = True
                        player_copy.statistics.save()
                    player_copy.save()

                # Overwrite the current roster with this new roster.
                scorebook.visiting_coach.roster = roster
                scorebook.visiting_coach.save()
                return HttpResponseRedirect('/edit-scorebook/')

        elif "publishScorebookModal" in str(request.POST):
            if scorebook is not None:
                home_score_count = len(list(scorebook.running_score.home.all()))
                visiting_score_count = len(
                    list(scorebook.running_score.visiting.all()))
                scorebook.home_score = home_score_count
                scorebook.visiting_score = visiting_score_count

                scorebook.is_published = True
                scorebook.home_coach.roster.save()
                scorebook.visiting_coach.roster.save()
                for player in scorebook.home_coach.roster.player_set.iterator():
                    player.team = scorebook.home_coach.roster
                    player.save()
                for player in scorebook.visiting_coach.roster.player_set.iterator():
                    player.team = scorebook.visiting_coach.roster
                    player.save()

                scorebook.save()
                scorebook = None
                scorebook_context["scorebook"] = None
                return HttpResponseRedirect('/')


        # User selected to clear the roster.
        elif "clearScorebookModal" in str(request.POST):
            if scorebook is not None:
                scorebook.delete()
                scorebook = None
                scorebook_context["scorebook"] = None
                return HttpResponseRedirect('/create-scorebook/')

    # Update the context with blank forms if the user enters the page.
    elif request.method == "GET":
        scorebook_context["home_running_score_form"] = ScorebookScoreForm(initial=initial_time)
        scorebook_context["visiting_running_score_form"] = ScorebookScoreForm(initial=initial_time)

        scorebook_context[
            "home_personal_foul_form"] = ScorebookPersonalFoulForm(initial=initial_time)
        scorebook_context[
            "home_technical_foul_form"] = ScorebookTechnicalFoulForm(initial=initial_time)
        scorebook_context[
            "visiting_personal_foul_form"] = ScorebookPersonalFoulForm(initial=initial_time)
        scorebook_context[
            "visiting_technical_foul_form"] = ScorebookTechnicalFoulForm(initial=initial_time)

        scorebook_context["home_timeout_form"] = ScorebookTimeoutForm(initial=initial_time)
        scorebook_context["visiting_timeout_form"] = ScorebookTimeoutForm(initial=initial_time)

        scorebook_context["home_add_player_form"] = ScorebookPlayerForm()
        scorebook_context["visiting_add_player_form"] = ScorebookPlayerForm()

    scorebook_context["scorebook"] = scorebook
    return render(request, "scorebook.html", scorebook_context)


def update_stats(request: HttpRequest) -> HttpResponse:
    # Parse GET request.
    player_id = request.GET["id"]
    stat_type = str(request.GET["stat_type"])

    # Get player.
    player = Player.objects.filter(id=player_id).first()

    # Update corresponding statistic.
    if stat_type in "player_statistics":
        stat = str(request.GET["stat"])
        stat_value = request.GET["stat_value"]

        if stat in "Q1":
            player.statistics.first_quarter = stat_value == "true"
        elif stat in "Q2":
            player.statistics.second_quarter = stat_value == "true"
        elif stat in "Q3":
            player.statistics.third_quarter = stat_value == "true"
        elif stat in "Q4":
            player.statistics.fourth_quarter = stat_value == "true"
        elif stat in "OT":
            player.statistics.overtime = stat_value == "true"
        elif stat in "Shots":
            player.statistics.shots = stat_value
        elif stat in "Goals":
            player.statistics.goals = stat_value
        elif stat in "Assists":
            player.statistics.assists = stat_value
        elif stat in "GroundBalls":
            player.statistics.ground_balls = stat_value

        player.statistics.save()

    elif stat_type in "goalie_saves":
        quarter = int(str(request.GET["quarter"]))
        saves_value = request.GET["saves_value"]

        if quarter == 0:
            player.saves.first_quarter = saves_value
        elif quarter == 1:
            player.saves.second_quarter = saves_value
        elif quarter == 2:
            player.saves.third_quarter = saves_value
        elif quarter == 3:
            player.saves.fourth_quarter = saves_value
        elif quarter == 4:
            player.saves.overtime = saves_value

        player.saves.save()

    return redirect(edit_scorebook)

@csrf_exempt
def update_timer(request: HttpRequest) -> HttpResponse:
    # Parse GET request.
    global scorebook_context, total_seconds
    #print(request.POST)
    scorebook_id = request.POST["id"]
    total_seconds = int(str(request.POST["seconds"]))

    # Get player.
    scorebook = Scorebook.objects.filter(id=scorebook_id).first()
    scorebook.time_elapsed = datetime.timedelta(minutes=total_seconds // 60,
                                                 seconds=total_seconds % 60)
    scorebook.save()
    scorebook_context["scorebook"] = scorebook
    scorebook_context["time"] = scorebook.time_elapsed

    return render(request, "edit_scorebook.html", scorebook_context)


@login_required
def scorebook_edit_score(request: HttpRequest, score_id: int) -> HttpResponse:
    score = Score.objects.get(id=score_id)
    initial = {
        "minutes": score.time.seconds // 60,
        "seconds": score.time.seconds % 60,
        "quarter": score.quarter,
        "goal_jersey": score.goal_number,
        "assist_jersey": score.assist_number,
    }
    initial.update(initial_time)
    if score.home_score:
        roster = scorebook.home_coach.roster
    else:
        roster = scorebook.visiting_coach.roster

    if score is not None:
        if request.method == "POST":
            form = running_score_form_factory(request, roster=roster, initial=initial_time)
            if form.is_valid():
                time = datetime.timedelta(minutes=form.cleaned_data["minutes"],
                                          seconds=form.cleaned_data["seconds"])
                score.time = time
                score.quarter = form.cleaned_data.get("quarter")
                score.goal_number = form.cleaned_data.get("goal_jersey")
                score.assist_number = form.cleaned_data.get("assist_jersey")
                score.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = running_score_form_factory(request, roster=roster,
                                          initial=initial)
        return render(request, "edit_score.html",
                      {"form": form, "id": score.id})
    else:
        return HttpResponse("Running Score Not Found")


@login_required
def scorebook_edit_personal_foul(request: HttpRequest,
                                 penalty_id: int) -> HttpResponse:
    penalty = Penalty.objects.get(id=penalty_id)
    initial = {
        "minutes": penalty.time.seconds // 60,
        "seconds": penalty.time.seconds % 60,
        "player_number": penalty.player_number,
        "infraction": penalty.infraction,
        "quarter": penalty.quarter,
    }
    initial.update(initial_time)
    if penalty.home_penalties:
        roster = scorebook.home_coach.roster
    else:
        roster = scorebook.visiting_coach.roster

    if penalty is not None:
        if request.method == "POST":
            form = penalty_form_factory(request, is_personal=True,
                                        roster=roster, initial=initial_time)
            if form.is_valid():
                time = datetime.timedelta(minutes=form.cleaned_data["minutes"],
                                          seconds=form.cleaned_data["seconds"])
                penalty.time = time
                penalty.player_number = form.cleaned_data.get("player_number")
                penalty.infraction = form.cleaned_data.get("infraction")
                penalty.quarter = form.cleaned_data.get("quarter")
                penalty.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = penalty_form_factory(request, is_personal=True, roster=roster,
                                    initial=initial)
        return render(request, "edit_personal_foul.html",
                      {"form": form, "id": penalty.id})
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_edit_technical_foul(request: HttpRequest,
                                  penalty_id: int) -> HttpResponse:
    penalty = Penalty.objects.get(id=penalty_id)
    initial = {
        "minutes": penalty.time.seconds // 60,
        "seconds": penalty.time.seconds % 60,
        "player_number": penalty.player_number,
        "infraction": penalty.infraction,
        "quarter": penalty.quarter,
    }
    initial.update(initial_time)
    if penalty.home_penalties:
        roster = scorebook.home_coach.roster
    else:
        roster = scorebook.visiting_coach.roster

    if penalty is not None:
        if request.method == "POST":
            form = penalty_form_factory(request, is_personal=False,
                                        roster=roster, initial=initial_time)
            if form.is_valid():
                penalty.player_number = form.cleaned_data.get("player_number")
                penalty.infraction = form.cleaned_data.get("infraction")
                penalty.quarter = form.cleaned_data.get("quarter")
                penalty.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = penalty_form_factory(request, is_personal=False, roster=roster,
                                    initial=initial)
        return render(request, "edit_technical_foul.html",
                      {"form": form, "id": penalty.id})
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_edit_timeout(request: HttpRequest,
                           timeout_id: int) -> HttpResponse:
    timeout = Timeout.objects.get(id=timeout_id)
    initial = {
        "minutes": timeout.time.seconds // 60,
        "seconds": timeout.time.seconds % 60,
        "quarter": timeout.quarter,
    }
    initial.update(initial_time)
    if timeout.home_timeouts:
        timeouts = timeout.home_timeouts.home
    else:
        timeouts = timeout.visiting_timeouts.visiting

    if timeout is not None:
        if request.method == "POST":
            form = timeout_form_factory(request, timeouts=timeouts, initial=initial_time)
            if form.is_valid():
                time = datetime.timedelta(minutes=form.cleaned_data["minutes"],
                                          seconds=form.cleaned_data["seconds"])
                timeout.time = time
                timeout.quarter = form.cleaned_data.get("quarter")
                timeout.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = timeout_form_factory(request, timeouts=timeouts, initial=initial)
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
    initial.update(initial_time)
    roster = player.team

    if player is not None:
        if request.method == "POST":
            form = player_form_factory(request, roster=roster, initial=initial_time)
            if form.is_valid():
                player.player_number = form.cleaned_data.get("player_number")
                player.first_name = form.cleaned_data.get("first_name")
                player.last_name = form.cleaned_data.get("last_name")
                player.position = form.cleaned_data.get("position")
                player.save()
                return HttpResponseRedirect("/edit-scorebook/")

        form = player_form_factory(request, roster=roster, initial=initial)
        return render(request, "edit_scorebook_player.html",
                      {"form": form, "id": player.id})
    else:
        return HttpResponse("Player Not Found")


@login_required
def scorebook_delete_score(request: HttpRequest, score_id: int) -> HttpResponse:
    score = Score.objects.filter(id=score_id).first()
    if score is not None:
        score.delete()
        return HttpResponseRedirect("/edit-scorebook/")
    else:
        return HttpResponse("Score Not Found")


@login_required
def scorebook_delete_penalty(request: HttpRequest,
                             penalty_id: int) -> HttpResponse:
    penalty = Penalty.objects.filter(id=penalty_id).first()
    if penalty is not None:
        penalty.delete()
        return HttpResponseRedirect("/edit-scorebook/")
    else:
        return HttpResponse("Penalty Not Found")


@login_required
def scorebook_delete_timeout(request: HttpRequest,
                             timeout_id: int) -> HttpResponse:
    timeout = Timeout.objects.filter(id=timeout_id).first()
    if timeout is not None:
        timeout.delete()
        return HttpResponseRedirect("/edit-scorebook/")
    else:
        return HttpResponse("Timeout Not Found")


@login_required
def scorebook_delete_player(request: HttpRequest,
                            player_id: int) -> HttpResponse:
    player = Player.objects.filter(id=player_id).first()
    if player is not None:
        player.delete()
        return HttpResponseRedirect("/edit-scorebook/")
    else:
        return HttpResponse("Player Not Found")


@login_required
def view_roster(request: HttpRequest) -> HttpResponse:
    # Since usernames are unique, find the coach's data from the QuerySet.
    coach = Coach.objects.filter(user=request.user).first()
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
                              {"player_entry_form": PlayerEntryForm(),
                               "starting_lineup_form": starting_lineup_form_factory(
                                   request, default=True),
                               "has_roster": True,
                               "roster": roster})

        return render(request, "roster.html",
                      {"form": RosterEntryForm(), "has_roster": False})

    # Otherwise, the Coach has established a Roster, so display it.
    else:
        # When the coach enters the player data, handle it here.
        if request.method == "POST":
            if "addPlayer" in str(request.POST):
                form = roster_player_form_factory(request, roster=coach.roster)
                if form.is_valid():
                    statistics = PlayerStatistics()
                    statistics.save()
                    saves = PlayerSaves()
                    saves.save()

                    if form.cleaned_data["profile_image"]:
                        profile_image = form.cleaned_data["profile_image"]
                    else:
                        profile_image = "profile_pictures/default.jpg"

                    player = Player(
                        profile_image=profile_image,
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
                        statistics=statistics,
                        saves=saves
                    )
                    player.save()

                    # Redirect to the root roster page so that the GET request isn't sent again upon refreshing the page.
                    return HttpResponseRedirect("/roster/")
                roster_context["player_entry_form"] = form
            else:
                roster_context["player_entry_form"] = PlayerEntryForm()

        if "startingLineup" in str(request.POST):
            form = starting_lineup_form_factory(request)
            if form.is_valid():
                starting_lineup = StartingLineup(
                    school=coach.roster.school,
                    team_name=coach.roster.team_name,
                    coach_first_name=coach.first_name,
                    coach_last_name=coach.last_name,
                    attacker_1=form.cleaned_data["attackmen"][0],
                    attacker_2=form.cleaned_data["attackmen"][1],
                    attacker_3=form.cleaned_data["attackmen"][2],
                    midfielder_1=form.cleaned_data["midfielders"][0],
                    midfielder_2=form.cleaned_data["midfielders"][1],
                    midfielder_3=form.cleaned_data["midfielders"][2],
                    defender_1=form.cleaned_data["defensemen"][0],
                    defender_2=form.cleaned_data["defensemen"][1],
                    defender_3=form.cleaned_data["defensemen"][2],
                    goalie=form.cleaned_data["goalie"])
                substitutes = Substitutes()
                substitutes.save()
                for player in list(form.cleaned_data["substitutes"]):
                    player.substitute = substitutes
                    player.save()

                starting_lineup.substitutes = substitutes
                starting_lineup.save()
                coach.starting_lineup = starting_lineup
                coach.save()

                return HttpResponseRedirect("/roster/")

            roster_context["starting_lineup_form"] = form
        else:
            roster_context[
                "starting_lineup_form"] = starting_lineup_form_factory(request,
                                                                       default=True)

        roster_context["players"] = coach.roster.player_set.all()
        roster_context["roster"] = coach.roster
        roster_context["starting_lineup"] = coach.starting_lineup

        return render(request, "roster.html", roster_context)


@login_required
def edit_player(request: HttpRequest, player_id: int) -> HttpResponse:
    player = Player.objects.get(id=player_id)
    initial = {
        "profile_image": player.profile_image,
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
            form = PlayerEntryForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data["profile_image"] is not None:
                    player.profile_image = form.cleaned_data["profile_image"]
                elif player.profile_image is not None:
                    pass
                else:
                    player.profile_image = "default.jpg"

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
    player = Player.objects.filter(id=player_id).first()
    if player is not None:
        player.delete()
        return HttpResponseRedirect("/roster/")
    else:
        return HttpResponse("Player Not Found")
