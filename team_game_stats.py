from typing import List

from player_game_stats import PlayerGameStats
from stats import Stats


class TeamGameStats:
    players_stats: List[PlayerGameStats]
    global_stats: Stats
