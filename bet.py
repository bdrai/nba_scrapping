class Bet:
    _bet_id: int
    team_home_id: str
    team_away_id: str
    bookmaker: str
    home_odd: float
    away_odd: float

    def __init__(self, odd_id, team_home_id, team_away_id, bookmaker, home_odd, away_odd):
        self._bet_id = odd_id
        self.team_home_id = team_home_id
        self.team_away_id = team_away_id
        self.bookmaker = bookmaker
        self.home_odd = home_odd
        self.away_odd = away_odd

    def is_in_db(self, cursor):
        """Tests if the Player is in the database."""
        cursor.execute(f"SELECT * FROM `Odd` WHERE odd_id = '{self._bet_id}';")
        result = cursor.fetchone()
        if result:
            return True
        return False

    def write_in_db(self, cursor):
        """Writes Player data in MySQL database."""
        query_insert = """
            INSERT INTO `Odd` (
                bet_id,
                team_home_id,
                team_away_id,
                bookmaker,
                home_odd,
                away_odd,
    
            ) VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self._bet_id, self.team_home_id, self.team_away_id, self.home_odd, self.away_odd))
