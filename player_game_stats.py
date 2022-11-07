from stats import Stats


class PlayerGameStats:
    player_id: str
    first_name: str
    last_name: str
    game_id: str
    is_starter: bool
    is_dnp: bool
    dnp_reason: str
    stats: Stats
