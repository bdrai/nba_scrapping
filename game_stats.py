from team_game_stats import TeamGameStats


class GameStats:
    game_id: str
    team1: TeamGameStats
    team2: TeamGameStats

    def __init__(self, game_id):
        self.game_id = game_id
        self.url_stats = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"

    def scraping_stats(self):
        pass

    def __str__(self):
        pass

