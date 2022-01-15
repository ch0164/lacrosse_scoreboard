from rest_framework import generics

from .models import Player
from .serializers import PlayerSerializer

# Create your views here.

class RosterView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer