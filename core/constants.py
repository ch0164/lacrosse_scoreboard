"""This file defines constants for the scoreboard."""

CLASS_STANDING_CHOICES = (
    ("FR", "Freshman"),
    ("SO", "Sophomore"),
    ("JR", "Junior"),
    ("SR", "Senior")
)

POSITION_CHOICES = (
    # Four main lacrosse positions.
    ("ATT", "Attacker"),
    ("MID", "Midfielder"),
    ("DEF", "Defender"),
    ("G", "Goalkeeper"),

    # Three specialized lacrosse positions.
    ("FOGO", "Faceoff Specialist"),  # "Face Off Get Off"
    ("LSM", "Long-Stick Midfielder"),
    ("SSDM", "Short-Stick Defensive Midfielder")
)

QUARTERS = (
    ("", ""),
    ("I", "First"),
    ("II", "Second"),
    ("III", "Third"),
    ("IV", "Fourth")
)