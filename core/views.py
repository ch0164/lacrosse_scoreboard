from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from core.forms import *
from core.models import *


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


# Registration view is defined in user_registration/views.py.

def view_scorebook(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebook.html")


@login_required
def edit_scorebook(request: HttpRequest) -> HttpResponse:
    return render(request, "scorebook.html", {"numbers": list(range(100))})


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
