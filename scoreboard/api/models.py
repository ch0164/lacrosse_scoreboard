from dataclasses import dataclass
from django.db import models

# Create your models here.
@dataclass
class Player(models.Model):
    first_name: str
    last_name: str
    player_number: int
    class_standing: str
    major: str
    position: str
    hometown: str
    height_feet: int
    height_inches: int
    weight_pounds: int
