
from typing import List

from player_game_stats import PlayerGameStats
from stats import Stats


class TeamGameStats:
    players_stats: List[PlayerGameStats]
    global_stats: Stats

    def __init__(self, global_stats):
        self.global_stats = global_stats
        self.players_stats = []

    def add_player_game_stats(self, player_game_stats: PlayerGameStats):
        self.players_stats.append(player_game_stats)

