from typing import List
from stats import Stats
from player_game_stats import PlayerGameStats
import pandas as pd


class TeamGameStats:
    game_id: str
    team_name: str
    players_stats: List[PlayerGameStats]
    global_stats: Stats

    def __init__(self, game_id):
        self.game_id = game_id
        self.players_stats = []

    def add_player_game_stats(self, player_game_stats: PlayerGameStats):
        self.players_stats.append(player_game_stats)

    def set_global_stats(self, global_stats):
        self.global_stats = global_stats

    def set_team_name(self, team_name):
        self.team_name = team_name

    def print_dataframe(self):
        """Print a pandas dataframe containing the box score for each game"""
        df_list = []
        for player_stat in self.players_stats:
            df_list.append([
                player_stat.full_name,
                player_stat.is_starter,
                player_stat.is_dnp,
                player_stat.dnp_reason,
                player_stat.position,
                *player_stat.stats.export_stats_in_list()
            ])
        df = pd.DataFrame(df_list, columns=['Full Name', 'IsStarter', 'IsDNP', 'DNPReason', 'POS', 'MIN', 'FGM',
                                            'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREP', 'REB', 'AST', 'STL',
                                            'BLK', 'TO', 'PF', '+/-', 'PTS']).set_index('Full Name')
        print(df.to_string())
