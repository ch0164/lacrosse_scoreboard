from rest_framework import generics
from .models import Player, Roster
from .serializers import PlayerSerializer, RosterSerializer

# Create your views here.
class PlayerView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class RosterView(generics.CreateAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer
