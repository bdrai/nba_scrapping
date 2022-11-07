class Game:
    id: str
    team1: str
    team2: str
    points1: int
    points2: int
    team1_record: str
    team2_record: str
    url_stats: str

    def __init__(self, id, team1, team2, points1, points2, team1_record, team2_record, url_stats, game_date):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.points1 = points1
        self.points2 = points2
        self.team1_record = team1_record
        self.team2_record = team2_record
        self.url_stats = url_stats
        self.game_date = game_date

    def __str__(self):
        return f"Game(team1={self.team1}, team2={self.team2}, points1={self.points1}, points2={self.points2}, " \
               f"team1_record='{self.team1_record}', team2_record='{self.team2_record}', url_stats={self.url_stats}, " \
               f"game_date={self.game_date})"

    def write_in_db(self):
        pass