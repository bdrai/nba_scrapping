class Bet:
    team_home_id: str
    team_away_id: str
    bookmaker: str
    home_odd: float
    away_odd: float

    def __init__(self, team_home_id, team_away_id, bookmaker, home_odd, away_odd):
        self.team_home_id = team_home_id
        self.team_away_id = team_away_id
        self.bookmaker = bookmaker
        self.home_odd = home_odd
        self.away_odd = away_odd

    def write_in_db(self, cursor):
        """Writes Player data in MySQL database."""
        query_insert = """
            INSERT INTO `Bet` (
                `date`,
                `team_home_id`,
                `team_away_id`,
                `home_odd`,
                `away_odd`,
                `bookmaker`
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self._bet_id, self.team_home_id, self.team_away_id, self.home_odd, self.away_odd))
