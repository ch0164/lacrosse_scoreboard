from rest_framework import generics
from .models import Player
from .serializers import PlayerSerializer

# Create your views here.

class RosterView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
