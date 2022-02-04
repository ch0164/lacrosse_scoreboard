from rest_framework import generics
from .models import Player, Roster
from .serializers import PlayerSerializer, RosterSerializer
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest, id) -> HttpResponse:
    user = User.objects.get(id=id)
    return HttpResponse(f"<h1>{user}</h1>")

def HomeView(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

def PublishedScorebooksView(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebooks.html")

def RosterView(request: HttpRequest) -> HttpResponse:
    players = Player.objects.all()
    return render(request, "roster.html", {"players": players})

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


def ScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "scorebook.html")

def EditScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "edit_scorebook.html")

def LoginView(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


class CreatePlayerView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class ListPlayerView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class CreateRosterView(generics.CreateAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer


class ListRosterView(generics.ListAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer
