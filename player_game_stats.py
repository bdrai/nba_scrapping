from stats import Stats


class PlayerGameStats:
    player_id: str
    game_id: str
    full_name: str
    is_starter: bool
    is_dnp: bool
    dnp_reason: str
    position: str
    stats: Stats

    def __init__(self, player_id, game_id, full_name, is_starter, is_dnp, dnp_reason, position, stats):
        self.player_id = player_id
        self.game_id = game_id
        self.full_name = full_name
        self.is_starter = is_starter
        self.is_dnp = is_dnp
        self.dnp_reason = dnp_reason
        self.position = position
        self.stats = stats

    def __str__(self):
        return ""