import datetime
from game_stats import GameStats

class Game:
    _id: str
    game_date: datetime.datetime
    # game_stats: GameStats


    def __init__(self, _id, game_date):
        self._id = _id
        self.game_date = game_date


    def __str__(self):
        return f"Game(id={self._id}, date={self.game_date})"

    def write_in_db(self):
        pass