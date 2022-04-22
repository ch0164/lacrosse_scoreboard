from core.models import *

def get_top_three(roster):
    if len(list(roster.player_set.all())) >= 3:

        players = list(roster.player_set.all())

        def player_average(player) -> float:
            return player.statistics.goals + 0.5 * player.statistics.assists

        # Sort players by descending player average.
        players.sort(reverse=True, key=player_average)
        return players[0:3]

    else:
        return None


def populate_quarter(cleaned_data):
    if "minutes" not in cleaned_data:
        return cleaned_data
    elif cleaned_data["minutes"] < 15:
        cleaned_data["quarter"] = "I"
    elif cleaned_data["minutes"] < 30:
        cleaned_data["quarter"] = "II"
    elif cleaned_data["minutes"] < 45:
        cleaned_data["quarter"] = "III"
    elif cleaned_data["minutes"] < 60:
        cleaned_data["quarter"] = "IV"
    else:
        cleaned_data["quarter"] = "OT"
    return cleaned_data


def copy_player(player: Player) -> Player:
    statistics = PlayerStatistics()
    statistics.save()
    saves = PlayerSaves()
    saves.save()
    return Player(profile_image=player.profile_image,
                  player_number=player.player_number,
                  first_name=player.first_name,
                  last_name=player.last_name,
                  position=player.position,
                  class_standing=player.class_standing,
                  weight_pounds=player.weight_pounds,
                  height_feet=player.height_feet,
                  height_inches=player.height_inches,
                  major=player.major,
                  hometown=player.hometown,
                  team=player.team,
                  statistics=statistics,
                  saves=saves)