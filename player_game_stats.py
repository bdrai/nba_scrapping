from stats import Stats


class PlayerGameStats:
    player_id: str
    game_id: str
    is_starter: bool
    is_dnp: bool
    dnp_reason: str
    position: str
    stats: Stats

    def __init__(self, player_id, game_id, is_starter, is_dnp, dnp_reason, position, stats):
        self.player_id = player_id
        self.game_id = game_id
        self.is_starter = is_starter
        self.is_dnp = is_dnp
        self.dnp_reason = dnp_reason
        self.position = position
        self.stats = stats

    def is_in_db(self, cursor):
        cursor.execute(f"""
            SELECT * FROM `PlayerGameStats` 
            WHERE player_id = {self.player_id} AND game_id = {self.game_id};
        """)
        if len(cursor.fetchall()) > 0:
            return True
        return False

    def write_in_db(self, cursor):
        if self.is_in_db(cursor):
            return
        query_insert = """
            INSERT INTO `PlayerGameStats` (
                player_id,
                game_id,
                `position`,
                is_starter,
                is_dnp,
                dnp_reason,
                `min`,
                fgm,
                fga,
                three_pts_m,
                three_pts_a,
                ftm,
                fta,
                oreb,
                dreb,
                reb,
                ast,
                stl,
                blk,
                `to`,
                pf,
                plus_minus,
                pts
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self.player_id, self.game_id, self.position, self.is_starter, self.is_dnp,
                                      self.dnp_reason, self.stats.min, self.stats.fgm, self.stats.fga,
                                      self.stats.three_pts_m, self.stats.three_pts_a, self.stats.ftm, self.stats.fta,
                                      self.stats.oreb, self.stats.dreb, self.stats.reb, self.stats.ast, self.stats.stl,
                                      self.stats.blk, self.stats.to, self.stats.pf, self.stats.plus_minus,
                                      self.stats.pts))

    def __str__(self):
        return f"PlayerID: {self.player_id} - GameID: {self.game_id} - Position: {self.position}"