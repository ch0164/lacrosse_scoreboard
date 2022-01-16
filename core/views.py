from rest_framework import generics
from .models import Player, Roster, User
from .serializers import PlayerSerializer, RosterSerializer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from .forms import UserForm


# Create your views here.
def index(request: HttpRequest, id) -> HttpResponse:
    user = User.objects.get(id=id)
    return HttpResponse(f"<h1>{user}</h1>")

def HomeView(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

def PublishedScorebooksView(request: HttpRequest) -> HttpResponse:
    return render(request, "published_scorebooks.html")

def RosterView(request: HttpRequest) -> HttpResponse:
    return render(request, "roster.html")

def ScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "scorebook.html")

def EditScorebookView(request: HttpRequest) -> HttpResponse:
    return render(request, "edit_scorebook.html")

def LoginView(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

def RegisterView(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User(email=email, username=username, password=password)
            user.save()

            return HttpResponseRedirect(f"/{user.id}")
    else:
        form = UserForm()
        
    return render(request, "register.html", {"form": form})


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
