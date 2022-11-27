import datetime
import pymysql.cursors
from env import Env


class Game:
    game_id: int
    game_date: datetime.datetime
    team_home_id: str
    team_away_id: str
    team_home_score: int
    team_away_score: int
    location: str
    arena: str

    def __init__(self, game_id, game_date, team_home_id, team_away_id, team_home_score,
                 team_away_score, location=None, arena=None):
        self.game_id = game_id
        self.game_date = game_date
        self.team_home_id = team_home_id
        self.team_away_id = team_away_id
        self.team_home_score = team_home_score
        self.team_away_score = team_away_score
        self.location = location
        self.arena = arena

    def write_game_in_db(self, cursor):
        cursor.execute(f"SELECT COUNT(*) FROM Game WHERE id = '{self.game_id}';")
        is_in_db = True if cursor.fetchone()[0] > 0 else False
        if is_in_db:
            return
        query_insert = """
            INSERT INTO `Game` (
                `id`,
                `date`,
                `team_home_id`,
                `team_away_id`,
                `team_home_score`,
                `team_away_score`,
                `location`,
                `arena`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self.game_id, self.game_date,
                                      self.team_home_id, self.team_away_id,
                                      self.team_home_score, self.team_away_score,
                                      self.location, self.arena))
        return

    def __str__(self):
        return f"{self.game_date}: {self.team_home_id.upper()} - {self.team_away_id.upper()}: " \
               f"{self.team_home_score} - {self.team_away_score}"


