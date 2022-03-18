from .models import Player, Roster, Coach
from .serializers import PlayerSerializer, RosterSerializer
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.forms import PlayerEntryForm

# Create your views here.
# CRUD: Create, Retrieve, Update, Delete
def HomeView(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

def PublishedScorebooksView(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebooks.html")

def RosterView(request: HttpRequest) -> HttpResponse:
    players = Player.objects.all()
    return render(request, "roster.html", {"players": players})

@login_required
def RosterView(request: HttpRequest) -> HttpResponse:
    # NOTE: Temporarily commented out (as well as contents of roster.html).
    #players = Player.objects.all()
    #return render(request, "roster.html", {"players": players})

    # TODO: Add players to the current coach's roster (not a temp one).
    # TODO: Coach needs to create a roster first.
    # Since usernames are unique, find the coach's data from the QuerySet.
    coach = Coach.objects.filter(user=request.user)[0]
    if coach.roster is None:
        temp_roster = Roster(team_name="UAH")
        temp_roster.save()
        coach.roster = temp_roster

    # When the coach enters the player data, handle it here.
    if request.method == "GET":
        form = PlayerEntryForm(request.GET)
        if form.is_valid():
            player = Player(
                player_number=request.GET.get("player_number"),
                first_name=request.GET.get("first_name"),
                last_name=request.GET.get("last_name"),
                position=request.GET.get("position"),
                class_standing=request.GET.get("class_standing"),
                weight_pounds=request.GET.get("weight_pounds"),
                height_feet=request.GET.get("height_feet"),
                height_inches=request.GET.get("height_inches"),
                major=request.GET.get("major"),
                hometown=request.GET.get("hometown"),
                team=coach.roster,
            )
            player.save()
            coach.roster.save()
            coach.save()

            print(coach.roster.player_set.all())
            print(player.team)

    form = PlayerEntryForm()
    return render(request, "roster.html", {"form": form})

def EditRoster(request: HttpRequest) -> JsonResponse:
    id = request.GET.get("id")
    type = request.GET.get("type")
    value = request.GET.get("value")

    player = Player.objects.get(id=id)
    if type == "player_number":
       player.player_number = value
    elif type == "name":
       first_name, last_name = tuple(value.split())
       player.first_name = first_name
       player.last_name = last_name
    elif type == "position":
        player.position = value
    elif type == "class_standing":
        player.class_standing = value
    elif type == "weight_pounds":
        player.weight_pounds = value
    elif type == "height_feet":
        player.height_feet = value
    elif type == "height_inches":
        player.height_inches = value
    elif type == "major":
        player.major = value
    elif type == "hometown":
        player.hometown = value

    player.save()
    return JsonResponse({"success": "Updated"})

def EditPlayer(request: HttpRequest, player_id: int) -> HttpResponse:
    player = Player.objects.get(id=player_id)
    if player is not None:
        return render(request, "edit_player.html", {"player": player})
    else:
        return HttpResponse("Player Not Found")

def ScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "scorebook.html")

def EditScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "edit_scorebook.html")

def LoginView(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

