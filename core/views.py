from rest_framework import generics
from django_tables2 import SingleTableView
from .models import Player, Roster
from .tables import PlayerTable
from .serializers import PlayerSerializer, RosterSerializer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
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
    if request.method == "POST":
        pass

    return render(request, "roster.html", {"players": players})

def ScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "scorebook.html")

def EditScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "edit_scorebook.html")

def LoginView(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

class PlayerListView(SingleTableView):
    model = Player
    table_class = PlayerTable
    template_name = "roster.html"


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
