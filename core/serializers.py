from .models import Coach, Player, Roster
from rest_framework import serializers


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            "id",
            "player_number",
            "first_name",
            "last_name",
            "position",
            "class_standing",
            "weight_pounds"
            "height_feet",
            "height_inches",
            "major",
            "hometown",
        )


class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        fields = (
            "id",
            "team_name",
            "school",
            "coach",
            "player_list",
            "win_count",
            "loss_count"
        )
