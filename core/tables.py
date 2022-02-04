import django_tables2 as tables
from .models import Player

class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap4.html"
        fields = ("first_name",
            "last_name",
            "player_number",
            "class_standing",
            "major",
            "position",
            "hometown",
            "height_feet",
            "height_inches",
            "weight_pounds",)
