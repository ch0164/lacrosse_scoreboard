from rest_framework import generics
from .models import Player, Roster
from .serializers import PlayerSerializer, RosterSerializer

# Create your views here.
class HomeView(generics.GenericAPIView):
    pass

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
