from .models import Player
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "player_number",
            "class_standing",
            "major",
            "position",
            "hometown",
            "height_feet",
            "height_inches",
            "weight_pounds"
        )
