from rest_framework_dataclasses.serializers import DataclassSerializer
from .models import Player

class PlayerSerializer(DataclassSerializer):
    class Meta:
        dataclass = Player
