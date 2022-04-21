"""This file defines constants for the scoreboard."""

CLASS_STANDING_CHOICES = (
    ("", ""),
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
    ("I", "First"),
    ("II", "Second"),
    ("III", "Third"),
    ("IV", "Fourth"),
    ("OT", "Overtime")
)

PERSONAL_FOULS = (
    ("SLASH", "Slashing"),
    ("TRIP", "Tripping"),
    ("X CHECK", "Cross Check"),
    ("CONDUCT", "Unsportsmanlike Conduct"),
    ("ROUGHNESS", "Unnecessary Roughness"),
    ("CROSSE", "Illegal Crosse"),
    ("B CHECK", "Illegal Body Check"),
    ("GLOVES", "Illegal Gloves"),
)

TECHNICAL_FOULS = (
    ("HOLD", "Holding"),
    ("INTERFERENCE", "Interference"),
    ("OOB", "Off Sides"),
    ("PUSH", "Pushing"),
    ("SCREEN", "Screening"),
    ("STALL", "Stalling"),
    ("WARD", "Warding Off"),
)

# Penalties_Home = (
#    ("PF", "Personal Foul")
#    ("TF", "Technical Foul")
#)

#Penalties_Away = (
#    ("PF", "Personal Foul")
#    ("TF", "Technical Foul")
#)